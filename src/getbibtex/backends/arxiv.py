import arxiv2bib
from bibtexparser.customization import splitname

from ..bibtex import bibtex_entry, get_citekey, normalize_name, protect_strings


__all__ = ['get_bibtex_from_arxiv_id']


def get_bibtex_from_arxiv_id(
    arxiv_id,
    debug_record=False,
    fix_uppercase=False,
    auto_protect=False,
    capitalize_field_names=True,
):
    try:
        arxiv_record = arxiv2bib.arxiv2bib_dict([arxiv_id])[arxiv_id]
    except KeyError:
        raise IOError("arXiv query returned no result")
    first_author = splitname(arxiv_record.authors[0])
    first_author_name = "".join(first_author["von"]) + "".join(
        first_author["last"]
    )
    citekey = get_citekey(first_author_name, journal=None, year=None)
    citekey += arxiv_id.replace("/", ".")
    author = " and ".join(
        [normalize_name(name) for name in arxiv_record.authors]
    )
    title = arxiv_record.title
    if fix_uppercase:
        title = title.capitalize()  # sentence-case
    else:
        title = protect_strings(title, auto_protect=auto_protect)
    journal = f"arXiv:{arxiv_id}"
    year = arxiv_record.year
    doi = f"10.48550/arXiv.{arxiv_id}"
    doi_url = f"https://doi.org/{doi}"
    return bibtex_entry(
        capitalize_field_names=capitalize_field_names,
        entrytype='article',
        citekey=citekey,
        author=author,
        title=title,
        journal=journal,
        year=year,
        url=doi_url,
    )
