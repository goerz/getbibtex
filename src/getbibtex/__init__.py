"""Top-level package for getbibtex."""
import pprint
import re
import sys

import click

from .backends.arxiv import get_bibtex_from_arxiv_id
from .backends.crossref import get_bibtex_from_doi, get_bibtex_from_query


__version__ = '0.1.0-dev'


RX_DOI = re.compile(r'10.\d{4,9}/[-._;()/:A-Z0-9]+', re.I)

RX_ARXIV_NEW = re.compile(r'arxiv.*?(\d{4}\.\d{4,}(v\d+)?)', re.I)
RX_ARXIV_OLD = re.compile(
    r"""
    ((
       math-ph
      |hep-ph
      |nucl-ex
      |nucl-th
      |gr-qc
      |astro-ph
      |hep-lat
      |quant-ph
      |hep-ex
      |hep-th
      |stat
        (\.(AP|CO|ML|ME|TH))?
      |q-bio
        (\.(BM|CB|GN|MN|NC|OT|PE|QM|SC|TO))?
      |cond-mat
        (\.(dis-nn|mes-hall|mtrl-sci|other|soft|stat-mech|str-el|supr-con))?
      |cs
        (\.(AR|AI|CL|CC|CE|CG|GT|CV|CY|CR|DS|DB|DL|DM|DC|GL|GR|HC|IR|IT|LG|LO|
          MS|MA|MM|NI|NE|NA|OS|OH|PF|PL|RO|SE|SD|SC))?
      |nlin
        (\.(AO|CG|CD|SI|PS))?
      |physics
        (\.(acc-ph|ao-ph|atom-ph|atm-clus|bio-ph|chem-ph|class-ph|comp-ph|
          data-an|flu-dyn|gen-ph|geo-ph|hist-ph|ins-det|med-ph|optics|ed-ph|
          soc-ph|plasm-ph|pop-ph|space-ph))?
      |math
          (\.(AG|AT|AP|CT|CA|CO|AC|CV|DG|DS|FA|GM|GN|GT|GR|HO|IT|KT|LO|MP|MG
          |NT|NA|OA|OC|PR|QA|RT|RA|SP|ST|SG))?
    )/\d{7}(v\d+)?)""",
    re.X,
)


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
    default=None,
    help=(
        "With --auto-protect, assume that titles returned by the backend "
        "are in sentence case, so that any words with capitals "
        "can be assumed to be proper nouns that need to be protected "
        "(enclosed in {}). With --no-auto-protect, the titles are used as "
        "they are returned by the backend, up ensuring that known proper "
        "nouns are protected. "
        "If neither option is given (default),  heuristics are applied "
        "to determine which words need to be protected."
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
    """Generate a BibTeX entry from the given query.

    Print a a sigle bibtex record to stdout, and any warnings/error messages to
    stderr.

    The ARGS are combined into a single query string. This must be a DOI, an
    arXiv identifier, a string (e.g. URL) containing a DOI or arXiv identifier,
    or a free-form query. Any space in the query string indicates a free-form
    query.
    """
    query = " ".join(args)
    doi = None
    try:
        is_doi = False
        is_arxiv = False
        if RX_ARXIV_NEW.search(query) or RX_ARXIV_OLD.search(query):
            is_arxiv = True
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
        if is_arxiv:
            match = None
            _rx = iter([RX_ARXIV_NEW, RX_ARXIV_OLD])
            while bool(match) is False:
                rx = next(_rx)
                match = rx.search(query)
            assert bool(match)
            arxiv_id = match.group(1)
            print(
                get_bibtex_from_arxiv_id(
                    arxiv_id,
                    debug_record=debug_record,
                    fix_uppercase=fix_uppercase,
                    auto_protect=auto_protect,
                    capitalize_field_names=capitalize_field_names,
                )
            )
        elif is_doi:
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
