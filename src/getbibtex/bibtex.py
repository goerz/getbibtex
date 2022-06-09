import re

from .journalnames import JOURNAL_INITIALS, JOURNAL_MACRO_TO_NAME


def _rx_word(word):
    """Regex for non-protected word that is not at beginning of string."""
    return re.compile(r'(?<!^)(?<!\{)\b' + word + r'\b(?!\})')


PROTECTED_WORDS = [(_rx_word('Schrödinger'), '{Schrödinger}')]


class _Raw(str):
    """A raw BibTeX string (that is, a macro)"""


def get_journal_initials(journal):
    if isinstance(journal, _Raw):
        journal = JOURNAL_MACRO_TO_NAME[journal]
    return JOURNAL_INITIALS.get(journal, ''.join(re.findall('[A-Z]', journal)))


def get_citekey(first_author, journal, year):
    parts = []
    if first_author is not None:
        parts.append(str(first_author))
    if journal is not None:
        parts.append(get_journal_initials(journal))
    if year is not None:
        parts.append(str(year))
    return ("".join(parts)).replace(" ", "")


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
