"""Tests for the arXiv backend.

The arXiv backend reaches the network through ``arxiv2bib.arxiv2bib_dict``.
These tests replace that single function with a stub so that the BibTeX
generation logic can be exercised offline.
"""

import types

import pytest

from getbibtex.backends import arxiv as arxiv_backend


def fake_record(authors, title, year):
    """Build a stand-in for an ``arxiv2bib`` reference record.

    Only the attributes accessed by ``get_bibtex_from_arxiv_id`` are provided.
    """
    return types.SimpleNamespace(authors=authors, title=title, year=year)


@pytest.fixture
def patch_arxiv(monkeypatch):
    """Patch ``arxiv2bib_dict`` to return a canned record for one arXiv id."""

    def _patch(arxiv_id, record):
        def fake_arxiv2bib_dict(ids):
            assert ids == [arxiv_id]
            # An unknown id yields an empty dict, mirroring arxiv2bib.
            return {arxiv_id: record} if record is not None else {}

        monkeypatch.setattr(
            arxiv_backend.arxiv2bib, "arxiv2bib_dict", fake_arxiv2bib_dict
        )

    return _patch


def test_get_bibtex_from_arxiv_id(patch_arxiv):
    """A typical arXiv record is rendered as an ``@article`` entry."""
    arxiv_id = "2205.15044"
    record = fake_record(
        authors=["Michael H. Goerz", "Daniel Basilewitsch"],
        title="Quantum Optimal Control via Semi-Automatic Differentiation",
        year=2022,
    )
    patch_arxiv(arxiv_id, record)

    result = arxiv_backend.get_bibtex_from_arxiv_id(arxiv_id)

    expected = (
        "@article{Goerz2205.15044,\n"
        "    Author = {Goerz, Michael H. and Basilewitsch, Daniel},\n"
        "    Title = {Quantum Optimal Control via Semi-Automatic "
        "Differentiation},\n"
        "    Journal = {arXiv:2205.15044},\n"
        "    Year = {2022},\n"
        "    Url = {https://doi.org/10.48550/arXiv.2205.15044},\n"
        "}"
    )
    assert result == expected


def test_get_bibtex_from_arxiv_id_fix_uppercase(patch_arxiv):
    """``fix_uppercase`` sentence-cases an all-caps title."""
    arxiv_id = "2205.15044"
    record = fake_record(
        authors=["Michael H. Goerz"],
        title="QUANTUM OPTIMAL CONTROL",
        year=2022,
    )
    patch_arxiv(arxiv_id, record)

    result = arxiv_backend.get_bibtex_from_arxiv_id(
        arxiv_id, fix_uppercase=True
    )

    assert "Title = {Quantum optimal control}," in result


def test_get_bibtex_from_arxiv_id_old_style(patch_arxiv):
    """An old-style identifier with a slash is sanitized in the citekey."""
    arxiv_id = "cond-mat/0411174"
    record = fake_record(
        authors=["Jane Doe"],
        title="A study of something",
        year=2004,
    )
    patch_arxiv(arxiv_id, record)

    result = arxiv_backend.get_bibtex_from_arxiv_id(arxiv_id)

    # The slash in the id becomes a dot in the citekey, but is kept verbatim
    # in the journal field.
    assert result.startswith("@article{Doecond-mat.0411174,")
    assert "Journal = {arXiv:cond-mat/0411174}," in result


def test_get_bibtex_from_arxiv_id_no_result(patch_arxiv):
    """An empty query result is turned into an ``IOError``."""
    arxiv_id = "0000.00000"
    patch_arxiv(arxiv_id, None)

    with pytest.raises(IOError, match="arXiv query returned no result"):
        arxiv_backend.get_bibtex_from_arxiv_id(arxiv_id)
