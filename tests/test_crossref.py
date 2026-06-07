"""Tests for the Crossref backend.

Most of the backend is pure logic that turns a Crossref ``message`` record into
a BibTeX entry; those functions are tested directly. The thin wrappers
``get_bibtex_from_doi`` and ``get_bibtex_from_query`` are the only parts that
hit the network (through ``habanero.Crossref``), and they are tested by
stubbing out the ``Crossref`` client.
"""

import types

import pytest

from getbibtex.backends import crossref as crossref_backend
from getbibtex.backends.crossref import (
    get_bibtex,
    get_bibtex_from_doi,
    get_bibtex_from_query,
    get_container_title,
    get_event_location,
    get_journal,
    get_names,
    get_page,
)
from getbibtex.bibtex import _Raw


# --- record builders --------------------------------------------------------


def article_record():
    """A minimal ``journal-article`` Crossref record."""
    return {
        'author': [{'family': 'Goerz', 'given': 'Michael H.'}],
        'title': ['Robust optimal control of a qubit'],
        'issued': {'date-parts': [[2022]]},
        'DOI': '10.1103/PhysRevLett.128.230502',
        'type': 'journal-article',
        'container-title': ['Phys. Rev. Lett.'],
        'page': '062308',
        'volume': '6',
        'issue': '1',
    }


def proceedings_record():
    """A minimal ``proceedings-article`` Crossref record."""
    return {
        'author': [{'family': 'Goerz', 'given': 'Michael'}],
        'editor': [{'family': 'Smith', 'given': 'John'}],
        'title': ['Some conference paper'],
        'issued': {'date-parts': [[2019]]},
        'DOI': '10.1000/xyz123',
        'type': 'proceedings-article',
        'container-title': ['Proceedings of the Big Conference'],
        'page': '10-20',
        'event': {'location': 'Berlin, Germany'},
    }


def book_chapter_record():
    """A minimal ``book-chapter`` Crossref record."""
    return {
        'author': [{'family': 'Doe', 'given': 'Jane'}],
        'editor': [{'family': 'Roe', 'given': 'Richard'}],
        'title': ['A chapter about things'],
        'issued': {'date-parts': [[2010]]},
        'DOI': '10.1000/book123',
        'type': 'book-chapter',
        'container-title': ['Handbook of Things'],
        'page': '100-150',
        'publisher': 'Springer',
        'volume': '2',
    }


# --- pure helpers -----------------------------------------------------------


def test_get_names():
    record = {
        'author': [
            {'family': 'Goerz', 'given': 'Michael H.'},
            {'family': 'Reich', 'given': 'Daniel M.'},
        ]
    }
    assert get_names(record, 'author') == (
        "Goerz, Michael H. and Reich, Daniel M."
    )
    # A missing field yields None rather than raising.
    assert get_names(record, 'editor') is None


def test_get_names_fix_uppercase():
    record = {'author': [{'family': 'GOERZ', 'given': 'MICHAEL H.'}]}
    assert get_names(record, 'author', fix_uppercase=True) == (
        "Goerz, Michael H."
    )


def test_get_journal_macro():
    """A known journal name is replaced by its macro (a raw BibTeX token)."""
    record = {'container-title': ['Phys. Rev. Lett.']}
    journal = get_journal(record)
    assert journal == 'prl'
    assert isinstance(journal, _Raw)


def test_get_journal_without_macros():
    record = {'container-title': ['Phys. Rev. Lett.']}
    journal = get_journal(record, use_journal_macros=False)
    assert journal == 'Phys. Rev. Lett.'
    assert not isinstance(journal, _Raw)


def test_get_journal_unknown_warns(capsys):
    """An unknown journal name is returned verbatim, with a warning."""
    record = {'container-title': ['Journal of Unknown Things']}
    journal = get_journal(record)
    assert journal == 'Journal of Unknown Things'
    assert "WARNING" in capsys.readouterr().err


def test_get_journal_missing():
    assert get_journal({}) is None


def test_get_page_variants():
    # Range, collapsed to the first page unless a range is allowed.
    assert get_page({'page': '10-20'}) == '10'
    assert get_page({'page': '10-20'}, allow_range=True) == '10--20'
    # An explicit article number takes precedence over a page.
    assert get_page({'article-number': '230502', 'page': '1-9'}) == '230502'
    # Nothing to report.
    assert get_page({}) is None


def test_get_container_title_and_event_location():
    record = proceedings_record()
    assert get_container_title(record) == 'Proceedings of the Big Conference'
    assert get_event_location(record) == 'Berlin, Germany'
    assert get_event_location({}) is None


# --- get_bibtex for each supported entry type -------------------------------


def test_get_bibtex_article():
    result = get_bibtex(article_record())
    expected = (
        "@article{GoerzPRL2022,\n"
        "    Author = {Goerz, Michael H.},\n"
        "    Title = {Robust optimal control of a qubit},\n"
        "    Journal = prl,\n"
        "    Year = {2022},\n"
        "    Doi = {10.1103/PhysRevLett.128.230502},\n"
        "    Pages = {062308},\n"
        "    Volume = {6},\n"
        "    Number = {1},\n"
        "}"
    )
    assert result == expected


def test_get_bibtex_article_no_journal_macros():
    result = get_bibtex(article_record(), use_journal_macros=False)
    assert "Journal = {Phys. Rev. Lett.}," in result


def test_get_bibtex_inproceedings():
    result = get_bibtex(proceedings_record())
    expected = (
        "@inproceedings{GoerzPBC2019,\n"
        "    Author = {Goerz, Michael},\n"
        "    Title = {Some conference paper},\n"
        "    Booktitle = {Proceedings of the Big Conference},\n"
        "    Year = {2019},\n"
        "    Doi = {10.1000/xyz123},\n"
        "    Pages = {10--20},\n"
        "    Address = {Berlin, Germany},\n"
        "    Editor = {Smith, John},\n"
        "}"
    )
    assert result == expected


def test_get_bibtex_incollection():
    result = get_bibtex(book_chapter_record())
    expected = (
        "@incollection{Doe2010,\n"
        "    Author = {Doe, Jane},\n"
        "    Title = {A chapter about things},\n"
        "    Booktitle = {Handbook of Things},\n"
        "    Year = {2010},\n"
        "    Doi = {10.1000/book123},\n"
        "    Pages = {100--150},\n"
        "    Editor = {Roe, Richard},\n"
        "    Publisher = {Springer},\n"
        "    Volume = {2},\n"
        "}"
    )
    assert result == expected


def test_get_bibtex_unsupported_type():
    record = article_record()
    record['type'] = 'dataset'
    with pytest.raises(NotImplementedError, match="dataset"):
        get_bibtex(record)


def test_get_bibtex_fix_uppercase():
    """``fix_uppercase`` sentence-cases the title and title-cases the names."""
    record = article_record()
    record['author'] = [{'family': 'GOERZ', 'given': 'MICHAEL H.'}]
    record['title'] = ['ROBUST OPTIMAL CONTROL OF A QUBIT']

    result = get_bibtex(record, fix_uppercase=True)
    assert "Author = {Goerz, Michael H.}," in result
    assert "Title = {Robust optimal control of a qubit}," in result


def test_get_container_title_missing():
    assert get_container_title({}) is None


def test_get_bibtex_missing_author_and_year():
    """A record without author or issued date omits those fields."""
    record = article_record()
    del record['author']
    del record['issued']

    result = get_bibtex(record)
    assert result.startswith("@article{PRL,")
    assert "Author" not in result
    assert "Year" not in result


# --- network wrappers (Crossref client stubbed out) -------------------------


class FakeCrossref:
    """Stand-in for ``habanero.Crossref`` that records ``works`` calls.

    ``response`` is either a fixed value returned for every ``works`` call, or
    a callable invoked with the call keyword arguments (so a test can return
    different payloads for an ``ids`` lookup versus a ``query_bibliographic``
    search).
    """

    def __init__(self, response):
        self._response = response
        self.calls = []

    def __call__(self):
        # The backend instantiates the client as ``Crossref()``; returning
        # ``self`` lets a single instance both configure and record the call.
        return self

    def works(self, **kwargs):
        self.calls.append(kwargs)
        if callable(self._response):
            return self._response(**kwargs)
        return self._response


@pytest.fixture
def patch_crossref(monkeypatch):
    """Install a :class:`FakeCrossref` returning ``response``; yield it."""

    def _patch(response):
        fake = FakeCrossref(response)
        monkeypatch.setattr(crossref_backend, "Crossref", fake)
        return fake

    return _patch


def test_get_bibtex_from_doi(patch_crossref):
    fake = patch_crossref({'status': 'ok', 'message': article_record()})

    result = get_bibtex_from_doi('10.1103/PhysRevLett.128.230502')

    assert result == get_bibtex(article_record())
    # The DOI was forwarded to the Crossref client.
    assert fake.calls == [{'ids': '10.1103/PhysRevLett.128.230502'}]


def test_get_bibtex_from_doi_bad_status(patch_crossref):
    patch_crossref({'status': 'error'})
    with pytest.raises(IOError, match="status 'error'"):
        get_bibtex_from_doi('10.1000/whatever')


def test_get_bibtex_from_doi_invalid_response(patch_crossref):
    # A dict without a 'status' key is rejected as invalid.
    patch_crossref({'unexpected': True})
    with pytest.raises(IOError, match="invalid"):
        get_bibtex_from_doi('10.1000/whatever')
    # A non-dict response is rejected too.
    patch_crossref(["not a dict"])
    with pytest.raises(IOError, match="returned"):
        get_bibtex_from_doi('10.1000/whatever')


def test_get_bibtex_from_doi_debug_record(patch_crossref, capsys):
    """``debug_record`` pretty-prints the record (minus references) to stderr."""
    record = article_record()
    record['reference'] = [{'key': 'ref1'}]  # should be stripped before print
    patch_crossref({'status': 'ok', 'message': record})

    get_bibtex_from_doi('10.1103/PhysRevLett.128.230502', debug_record=True)

    err = capsys.readouterr().err
    assert 'Robust optimal control of a qubit' in err
    assert 'ref1' not in err


def test_get_bibtex_from_doi_content_negotiation(patch_crossref, monkeypatch):
    """Unsupported types fall back to habanero content negotiation."""
    record = article_record()
    record['type'] = 'dataset'
    patch_crossref({'status': 'ok', 'message': record})

    fake_cn = types.SimpleNamespace(
        content_negotiation=lambda ids: "RAW BIBTEX FOR %s" % ids
    )
    monkeypatch.setattr(crossref_backend.habanero, "cn", fake_cn)

    result = get_bibtex_from_doi('10.1000/dataset')
    assert result == "RAW BIBTEX FOR 10.1000/dataset"


def test_get_bibtex_from_query(patch_crossref):
    fake = patch_crossref(
        {'status': 'ok', 'message': {'items': [article_record()]}}
    )

    result = get_bibtex_from_query('robust optimal control qubit')

    assert result == get_bibtex(article_record())
    assert fake.calls == [
        {'query_bibliographic': 'robust optimal control qubit', 'limit': 1}
    ]


def test_get_bibtex_from_query_debug_record(patch_crossref, capsys):
    """``debug_record`` also works for the query wrapper (no references key)."""
    patch_crossref(
        {'status': 'ok', 'message': {'items': [article_record()]}}
    )

    get_bibtex_from_query('robust optimal control', debug_record=True)

    assert 'Robust optimal control of a qubit' in capsys.readouterr().err


def test_get_bibtex_from_query_unsupported_without_doi(patch_crossref):
    """A query hit with an unsupported type and no DOI re-raises."""
    record = article_record()
    record['type'] = 'dataset'
    del record['DOI']
    patch_crossref({'status': 'ok', 'message': {'items': [record]}})

    with pytest.raises(NotImplementedError):
        get_bibtex_from_query('some dataset')


def test_get_bibtex_from_query_unsupported_with_doi(patch_crossref):
    """An unsupported query hit with a DOI falls back to a DOI lookup.

    The query returns an unsupported record that nonetheless carries a DOI;
    the backend then re-queries Crossref by that DOI, which here resolves to a
    supported article.
    """
    unsupported = article_record()
    unsupported['type'] = 'dataset'

    def respond(**kwargs):
        if 'query_bibliographic' in kwargs:
            return {'status': 'ok', 'message': {'items': [unsupported]}}
        # The follow-up ``ids=`` lookup resolves to a supported article.
        return {'status': 'ok', 'message': article_record()}

    fake = patch_crossref(respond)

    result = get_bibtex_from_query('robust optimal control')

    assert result == get_bibtex(article_record())
    # Two calls: the search, then the DOI lookup it fell back to.
    assert fake.calls == [
        {'query_bibliographic': 'robust optimal control', 'limit': 1},
        {'ids': '10.1103/PhysRevLett.128.230502'},
    ]
