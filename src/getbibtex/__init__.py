"""Top-level package for getbibtex."""
import pprint
import re
import sys

import click

from .backends.crossref import get_bibtex_from_doi, get_bibtex_from_query


__version__ = '0.1.0-dev'


RX_DOI = re.compile(r'10.\d{4,9}/[-._;()/:A-Z0-9]+', re.I)


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
