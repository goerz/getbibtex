import pprint
import re
import sys

import habanero
from habanero import Crossref

from ..bibtex import _Raw, bibtex_entry, get_citekey, protect_strings
from ..journalnames import JOURNAL_NAME_TO_MACRO


__all__ = ['get_bibtex_from_doi', 'get_bibtex_from_query']


def get_names(crossref_record, field, fix_uppercase=False):
    """Extract (author/editor) names from the Crossref record."""
    try:
        name_records = crossref_record[field]
    except KeyError:
        return None
    if fix_uppercase:
        return " and ".join(
            [
                f"{a['family'].title()}, {a['given'].title()}"
                for a in name_records
            ]
        )
    else:
        return " and ".join(
            [f"{a['family']}, {a['given']}" for a in name_records]
        )


def get_journal(crossref_record, use_journal_macros=True):
    """Extract journal from the Grossref record.

    If `use_journal_macros` is True, replace, return a macro name for the
    journal if possible.
    """
    keys = ['short-container-title', 'container-title']
    name_candidates = [
        name for key in keys for name in crossref_record.get(key, [])
    ]
    if use_journal_macros:
        for journal_name in name_candidates:
            if journal_name in JOURNAL_NAME_TO_MACRO:
                return _Raw(JOURNAL_NAME_TO_MACRO[journal_name])
        print(
            "WARNING: No macro name for %s"
            % ", ".join(
                [name for name in name_candidates if name is not None]
            ),
            file=sys.stderr,
        )
    for journal_name in name_candidates:
        if journal_name is not None:
            return journal_name
    return None


def get_container_title(crossref_record):
    keys = ['short-container-title', 'container-title']
    name_candidates = [
        name for key in keys for name in crossref_record.get(key, [])
    ]
    for name in name_candidates:
        if name is not None:
            return name
    return None


def get_page(crossref_record, allow_range=False):
    """Get page or article number from Crossref record."""
    try:
        page = crossref_record['article-number']
    except KeyError:
        page = crossref_record.get('page', None)
    if page is not None:
        range_match = re.match(r'(\w+)\s*(-|--|---|–|——)\s*(\w+)', page)
        if range_match:
            if allow_range:
                # normalize
                page = range_match.group(1) + '--' + range_match.group(3)
            else:
                page = range_match.group(1)
    return page


def get_event_location(crossref_record):
    try:
        return crossref_record['event']['location']
    except KeyError:
        return None


def get_bibtex(
    crossref_record,
    auto_protect=False,
    fix_uppercase=False,
    capitalize_field_names=True,
    use_journal_macros=True,
):
    """Generate a BibTeX entry for the given Crossref record.

    Args:
        crossref_record (dict): Crossref record
        auto_protect (bool): If True, assume that titles in the Crossref record
            are in sentence case, not in title case. That is, things that look
            like proper nouns in titles should be protected (enclosed in
            braces). Otherwise, only entries in PROTECTED_WORDS will be
            protected.
        fix_uppercase (bool): If True, fix the case of any author or editor
            names and the title. This is for records that contain all-uppercase
            entries for these fields. The result is not guaranteed to be
            perfect, and may require small manual corrections.
        use_journal_macros (bool): If True, use macro names for journals if
            possible (see `JOURNAL_MACRO_TO_NAME`)
    """
    try:
        first_author = crossref_record['author'][0]['family'].capitalize()
    except (KeyError, IndexError):
        first_author = None
    author = get_names(crossref_record, 'author', fix_uppercase=fix_uppercase)
    if fix_uppercase:
        title = crossref_record.get('title', [None])[0]
        if title is not None:
            title = title.capitalize()  # sentence-case
    else:
        title = protect_strings(
            crossref_record.get('title', [None])[0], auto_protect=auto_protect
        )
    try:
        year = crossref_record['issued']['date-parts'][0][0]
    except (KeyError, IndexError):
        year = None
    doi = crossref_record.get('DOI', None)
    crossreftype = crossref_record.get('type', None)
    crossreftype_to_entrytype = {
        'journal-article': 'article',
        'proceedings-article': 'inproceedings',
        'book-chapter': 'incollection',
    }
    entrytype = crossreftype_to_entrytype.get(crossreftype, None)
    if entrytype == 'article':
        journal = get_journal(
            crossref_record, use_journal_macros=use_journal_macros
        )
        citekey = get_citekey(first_author, journal, year)
        pages = get_page(crossref_record, allow_range=False)
        volume = crossref_record.get('volume', None)
        number = crossref_record.get('issue', None)
        return bibtex_entry(
            capitalize_field_names=capitalize_field_names,
            entrytype=entrytype,
            citekey=citekey,
            author=author,
            title=title,
            journal=journal,
            year=year,
            doi=doi,
            pages=pages,
            volume=volume,
            number=number,
        )
    elif entrytype == 'inproceedings':
        conference = get_container_title(crossref_record)
        citekey = get_citekey(first_author, conference, year)
        pages = get_page(crossref_record, allow_range=True)
        location = get_event_location(crossref_record)
        editor = get_names(
            crossref_record, 'editor', fix_uppercase=fix_uppercase
        )
        return bibtex_entry(
            capitalize_field_names=capitalize_field_names,
            entrytype=entrytype,
            citekey=citekey,
            author=author,
            title=title,
            booktitle=conference,
            year=year,
            doi=doi,
            pages=pages,
            address=location,
            editor=editor,
        )
    elif entrytype == 'incollection':
        citekey = get_citekey(first_author, None, year)
        pages = get_page(crossref_record, allow_range=True)
        editor = get_names(crossref_record, 'editor')
        booktitle = get_container_title(crossref_record)
        publisher = crossref_record.get('publisher', None)
        volume = crossref_record.get('volume', None)
        return bibtex_entry(
            entrytype=entrytype,
            citekey=citekey,
            author=author,
            title=title,
            booktitle=booktitle,
            year=year,
            doi=doi,
            pages=pages,
            editor=editor,
            publisher=publisher,
            volume=volume,
        )
    else:
        raise NotImplementedError(
            "Records of crossref-type %r are currently not supported"
            % (crossreftype)
        )


def debug_crossref_record(crossref_record):
    """Pretty-print the given JSON record to stderr."""
    crossref_record = crossref_record.copy()
    try:
        # including all references makes the record very verbose
        del crossref_record['reference']
    except KeyError:
        pass
    pprint.pprint(crossref_record, stream=sys.stderr)


def _check_response(res):
    if isinstance(res, dict):
        if 'status' in res:
            if res['status'] != 'ok':
                raise IOError(
                    "Crossref query returned status %r" % res['status']
                )
        else:
            raise IOError("Crossref query returned invalid %r" % res)
    else:
        raise IOError("Crossref query returned %r" % res)


def get_bibtex_from_doi(
    doi,
    debug_record=False,
    fix_uppercase=False,
    auto_protect=False,
    capitalize_field_names=True,
    use_journal_macros=True,
):
    """Generate a BibTeX entry for the given DOI."""
    cr = Crossref()
    res = cr.works(ids=doi)
    _check_response(res)
    crossref_record = res['message']
    if debug_record:
        debug_crossref_record(crossref_record)
    try:
        return get_bibtex(
            crossref_record,
            fix_uppercase=fix_uppercase,
            auto_protect=auto_protect,
            capitalize_field_names=capitalize_field_names,
            use_journal_macros=use_journal_macros,
        )
    except NotImplementedError as exc_info:
        print("WARNING: %s" % exc_info, file=sys.stderr)
        return habanero.cn.content_negotiation(ids=doi)


def get_bibtex_from_query(
    query,
    debug_record=False,
    fix_uppercase=False,
    auto_protect=False,
    capitalize_field_names=True,
    use_journal_macros=True,
):
    """Generate a BibTeX entry for the given Crossref search query."""
    cr = Crossref()
    res = cr.works(query_bibliographic=query, limit=1)
    _check_response(res)
    crossref_record = res['message']['items'][0]
    if debug_record:
        debug_crossref_record(crossref_record)
    try:
        return get_bibtex(
            crossref_record,
            fix_uppercase=fix_uppercase,
            auto_protect=auto_protect,
            capitalize_field_names=capitalize_field_names,
            use_journal_macros=use_journal_macros,
        )
    except NotImplementedError:
        # Note that we can't fall back to content negotiation directly, due to
        # https://github.com/sckott/habanero/issues/83
        if 'DOI' in crossref_record:
            return get_bibtex_from_doi(crossref_record['DOI'])
        else:
            raise
