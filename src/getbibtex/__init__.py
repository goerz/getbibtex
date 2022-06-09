"""Top-level package for getbibtex."""
import pprint
import re
import sys

import click
import habanero
from habanero import Crossref


__version__ = '0.1.0-dev'


# The JOURNAL_MACRO_TO_NAME must match the defined macros (@string) in your
# bibtex file
#
# r !./get_macros_as_dict.py refs.bib
JOURNAL_MACRO_TO_NAME = {
    'aamop': 'Adv. At. Mol. Opt. Phys.',
    'aarc': 'Autom. Rem. Contr.',
    'ac': 'Anal. Chem.',
    'acie': 'Angew. Chem. Int. Ed.',
    'aipa': 'AIP Advances',
    'ajp': 'Am. J. Phys.',
    'algo': 'Algorithmica',
    'ao': 'Appl. Opt.',
    'ap': 'Adv. Phys.',
    'apb': 'Appl. Phys. B',
    'apl': 'Appl. Phys. Lett.',
    'apx': 'Adv. Phys. X',
    'arpc': 'Annu. Rev. Phys. Chem.',
    'astrocomp': 'Astron. Comput.',
    'atms': 'ACM Trans. Math. Softw.',
    'avsqs': 'AVS Quantum Sci.',
    'bit': 'BIT',
    'bstj': 'Bell System Tech. J.',
    'cacm': 'Commun. ACM',
    'ccyb': 'Control Cybern.',
    'cmp': 'Commun. Math. Phys.',
    'computj': 'Comput. J.',
    'contp': 'Contemp. Phys.',
    'cp': 'Chem. Phys.',
    'cpam': 'Commun. Pur. Appl. Math.',
    'cpc': 'Comput. Phys. Commun.',
    'cpl': 'Chem. Phys. Lett.',
    'cse': 'Comput. Sci. Eng.',
    'csj': 'CEAS Space J.',
    'ecyb': 'Engrg. Cybernetics',
    'ejc': 'Eur. J. Control',
    'ejp': 'Eur. J. Phys.',
    'electr': 'Electronics',
    'entr': 'Entropy',
    'epjb': 'Eur. Phys. J. B',
    'epjd': 'Eur. Phys. J. D',
    'epjp': 'Eur. Phys. J. Plus',
    'epjqt': 'EPJ Quantum Technol.',
    'epl': 'Europhys. Lett.',
    'farad': 'Faraday Disc.',
    'foundphys': 'Found. Phys.',
    'fp': 'Fortschr. Phys.',
    'icta': 'IET Control Theory Appl.',
    'ijqi': 'Int. J. Quantum Inform.',
    'ijtp': 'Int. J. Theor. Phys.',
    'imajam': 'IMA J. Appl. Math.',
    'ip': 'Inverse Problems',
    'itac': 'IEEE Trans. Automat. Contr.',
    'itas': 'IEEE Trans. on Appl. Superc.',
    'jap': 'J. Appl. Phys.',
    'jcmpp': 'J. Comput. Phys.',
    'jcp': 'J. Chem. Phys.',
    'jcpm': 'J. Phys. Condens. Matter',
    'jcss': 'J. Comput. System Sci.',
    'jctn': 'J. Comput. Theor. Nanos.',
    'jlum': 'J. Lumin.',
    'jmo': 'J. Mod. Opt.',
    'jmp': 'J. Math. Phys.',
    'jmr': 'J. Magnet. Res.',
    'jmra': 'J. Magnet. Res. A',
    'job': 'J. Optics B',
    'jors': 'J. Open Res. Softw.',
    'josab': 'J. Opt. Soc. Am. B',
    'jota': 'J. Optim. Theor. Appl.',
    'jpa': 'J. Phys. A',
    'jpamt': 'J. Phys. A: Math. Theor.',
    'jpb': 'J. Phys. B',
    'jpc': 'J. Phys. Chem.',
    'jpca': 'J. Phys. Chem. A',
    'jpcm': 'J. Phys.: Condens. Matter',
    'mc': 'Math. Comput.',
    'mlst': 'Mach. Learn.: Sci. Technol.',
    'nams': 'Notices Amer. Math. Soc.',
    'nat': 'Nature',
    'natcom': 'Nat. Commun.',
    'natmeth': 'Nat. Methods',
    'natnano': 'Nat. Nano.',
    'natphot': 'Nat. Photon.',
    'natphys': 'Nat. Phys.',
    'njp': 'New J. Phys.',
    'npjqi': 'npj Quantum Inf',
    'oc': 'Opt. Comm.',
    'os': 'Opt. Spectr.',
    'physd': 'Physica D',
    'physrep': 'Phys. Rep.',
    'pire': 'Proc. IRE',
    'pl': 'Phys. Lett.',
    'pla': 'Phys. Lett. A',
    'plms': 'Proc. Lond. Math. Soc.',
    'pnas': 'Proc. Natl. Acad. Sci. U.S.A',
    'pr': 'Phys. Rev.',
    'pra': 'Phys. Rev. A',
    'prapl': 'Phys. Rev. Applied',
    'prb': 'Phys. Rev. B',
    'prc': 'Phys. Rev. C',
    'prd': 'Phys. Rev. D',
    'pre': 'Phys. Rev. E',
    'prl': 'Phys. Rev. Lett.',
    'prsa': 'Proc. R. Soc. A',
    'prx': 'Phys. Rev. X',
    'prxq': 'PRX Quantum',
    'ps': 'Phys. Scripta',
    'pt': 'Phys. Today',
    'ptrsa': 'Phil. Trans. R. Soc. A',
    'qam': 'Q. Appl. Math.',
    'qic': 'Quantum Info. Comput.',
    'qip': 'Quantum Inf. Process.',
    'qso': 'Quantum Semiclass. Opt.',
    'qst': 'Quantum Sci. Technol.',
    'quant': 'Quantum',
    'rmp': 'Rev. Mod. Phys.',
    'rpp': 'Rep. Prog. Phys.',
    'rsi': 'Rev. Sci. Instr.',
    'sci': 'Science',
    'sciam': 'Sci. Am.',
    'siamjc': 'SIAM J. Comput.',
    'siamjsc': 'SIAM J. Sci. Comput.',
    'siamrev': 'SIAM Rev.',
    'sp': 'Sig. Process.',
    'spp': 'SciPost Phys.',
    'sr': 'Sci. Rep.',
    'sst': 'Supercond. Sci. Technol.',
    'widm': 'WIREs Data Mining Knowl Discov.',
    'zp': 'Z. Phys.',
}


# JOURNAL_NAME_TO_MACRO is the inverse mapping of JOURNAL_MACRO_TO_NAME...
JOURNAL_NAME_TO_MACRO = {
    val: key for (key, val) in JOURNAL_MACRO_TO_NAME.items()
}
# ... with some aliases:
JOURNAL_NAME_TO_MACRO.update(
    {
        'J. Phys. B: At. Mol. Opt. Phys.': 'jpb',
        'The Journal of Chemical Physics': 'jcp',
    }
)

# In most cases, we get the journal initials simply by taking all the caps from
# the name. The following are some exceptions
JOURNAL_INITIALS = {
    'ACM Trans. Math. Softw.': 'ATMS',
    'CEAS Space J.': 'CSJ',
    'IEEE Trans. on Appl. Superc.': 'ITAS',
    'IEEE Trans. Automat. Contr.': 'ITAC',
    'npj Quantum Inf': 'NPJQI',
    'SIAM J. Comput.': 'SJC',
    'SIAM J. Sci. Comput.': 'SJSC',
    'SIAM Rev.': 'SR',
}

RX_DOI = re.compile(r'10.\d{4,9}/[-._;()/:A-Z0-9]+', re.I)


def _rx_word(word):
    """Regex for non-protected word that is not at beginning of string."""
    return re.compile(r'(?<!^)(?<!\{)\b' + word + r'\b(?!\})')


PROTECTED_WORDS = [(_rx_word('Schrödinger'), '{Schrödinger}')]


class _Raw(str):
    """A raw BibTeX string (that is, a macro)"""


def bibtex_entry(entrytype, citekey, *, capitalize_field_names=True, **kwargs):
    """Generate a multi-line BibTeX database entry."""
    entrytype = entrytype.lower()
    allowed_entrytypes = ['article', 'inproceedings', 'incollection']
    if entrytype not in allowed_entrytypes:
        raise ValueError("Cannot generate bibtex for entrytype %r" % entrytype)
    lines = []
    lines.append('@%s{%s,' % (entrytype, citekey))
    for (key, val) in kwargs.items():
        if capitalize_field_names:
            key = key.title()  # capitalize first letter
        else:
            key = key.lower()
        if val is not None:
            if isinstance(val, _Raw):
                lines.append('    %s = %s,' % (key, val))
            else:
                lines.append('    %s = {%s},' % (key, val))
    lines.append('}')
    return "\n".join(lines)


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


def get_event_location(crossref_record):
    try:
        return crossref_record['event']['location']
    except KeyError:
        return None


def get_journal_initials(journal):
    if isinstance(journal, _Raw):
        journal = JOURNAL_MACRO_TO_NAME[journal]
    return JOURNAL_INITIALS.get(journal, ''.join(re.findall('[A-Z]', journal)))


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


def get_citekey(first_author, journal, year):
    parts = []
    if first_author is not None:
        parts.append(str(first_author))
    if journal is not None:
        parts.append(get_journal_initials(journal))
    if year is not None:
        parts.append(str(year))
    return ("".join(parts)).replace(" ", "")


def protect_strings(s, auto_protect=False):
    if s is not None:
        s = s.replace("\n", "\\\\")
        if auto_protect:
            # https://stackoverflow.com/questions/7609880
            rx_proper_nouns = re.compile(
                r'''
                (?<!^)                  # Do not match at beginning of string
                (?<!\{)                 # Ignore words already protected
                \b                      # Word boundary (\w -> \W)
                (\w*[A-Z]\w+)           # Word containing a capital letter
                \b                      # Word boundary (\w -> \W)
                (?!\})                  # Ignore words already protected
                ''',
                re.X,
            )
            s = rx_proper_nouns.sub(r'{\1}', s)
        for (rx, repl) in PROTECTED_WORDS:
            s = rx.sub(repl, s)
    return s


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
        first_author = crossref_record['author'][0]['family'].title()
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


def _check_response(res):
    if isinstance(res, dict):
        if 'status' in res:
            if res['status'] != 'ok':
                raise IOError("Crossref query returned status" % res['status'])
        else:
            raise IOError("Crossref query returned invalid %r" % res)
    else:
        raise IOError("Crossref query returned %r" % res)


def debug_crossref_record(crossref_record):
    """Pretty-print the given JSON record to stderr."""
    crossref_record = crossref_record.copy()
    try:
        # including all references makes the record very verbose
        del crossref_record['reference']
    except KeyError:
        pass
    pprint.pprint(crossref_record, stream=sys.stderr)


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


@click.command()
@click.help_option('--help', '-h')
@click.option(
    '--debug-record', is_flag=True, help="Print the crossref record to stderr"
)
@click.option(
    '--fix-uppercase',
    is_flag=True,
    help=(
        "Fix records that contain all-uppercase authors or titles. This "
        "override --auto-protect."
    ),
)
@click.option(
    '--auto-protect/--no-auto-protect',
    default=True,
    help=(
        "With --auto-protect (default), assume that titles in the Crossref "
        "record are in proper sentence case, so that any words with capitals "
        "can be assumed to be proper nouns that need to be protected "
        "(enclosed in {})."
    ),
)
@click.option(
    '--capitalize-field-names/--no-capitalize-field-names',
    default=True,
    help=(
        "With --capitalize-field-names (default), capitalize the first "
        "letter of all BibTeX field names."
    ),
)
@click.option(
    '--use-journal-macros/--no-use-journal-macros',
    default=True,
    help=(
        "With --use-journal-macros (default), use journal macros for known "
        "journal names, e.g. `prl` for 'Phys. Rev. Lett.'"
    ),
)
@click.argument('args', nargs=-1, required=True)
def main(
    debug_record,
    fix_uppercase,
    auto_protect,
    capitalize_field_names,
    use_journal_macros,
    args,
):
    """Query the Crossref database and generate a BibTeX entry.

    Print a a sigle bibtex record to stdout, and any warnings/error messages to
    stderr.

    The ARGS are combined into a single query string. This must be a DOI, a
    string (e.g. URL) containing a DOI, or a free-form query. Any space in the
    query string indicates a free-form query.
    """
    query = " ".join(args)
    doi = None
    try:
        if ' ' in query:
            is_doi = False
        else:
            is_doi = True
            doi = query
            if not doi.startswith('10.'):
                # Handle e.g. URLs
                rx_match = RX_DOI.search(query)
                if rx_match:
                    doi = rx_match.group(0)
                else:
                    is_doi = False
        if is_doi:
            print(
                get_bibtex_from_doi(
                    doi=doi,
                    debug_record=debug_record,
                    fix_uppercase=fix_uppercase,
                    auto_protect=auto_protect,
                    capitalize_field_names=capitalize_field_names,
                    use_journal_macros=use_journal_macros,
                )
            )
        else:
            print(
                get_bibtex_from_query(
                    query=query,
                    debug_record=debug_record,
                    fix_uppercase=fix_uppercase,
                    auto_protect=auto_protect,
                    capitalize_field_names=capitalize_field_names,
                    use_journal_macros=use_journal_macros,
                )
            )
        return 0
    except (NotImplementedError, IOError) as exc_info:
        print("ERROR: %s" % exc_info, file=sys.stderr)
        return 1
