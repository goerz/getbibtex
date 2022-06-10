import re

from bibtexparser.customization import splitname
from unidecode import unidecode

from .journalnames import JOURNAL_INITIALS, JOURNAL_MACRO_TO_NAME


def _rx_word(word):
    """Regex for non-protected word that is not at beginning of string."""
    return re.compile(r'(?<!^)(?<!\{)\b' + word + r'\b(?!\})')


PROTECTED_WORDS = """
Schrödinger Rydberg Krotov Bose Einstein Dirac NMR GRAPE CRAB
""".split()

_PROTECTED_WORDS = [
    (_rx_word(word), '{' + word + '}') for word in PROTECTED_WORDS
]


# We define some ascii versions of unicode author last names. These override
# unidecode, which doesn't translate German umlauts, e.g. "ü" to "ue". This is
# for good reason (since umlauts/diaeresis is also used in other languages that
# don't use German transcription), we we define some German names with umlauts
# as special cases
NAME_UNICODE_MAP = {"Müller": "Mueller"}

# https://stackoverflow.com/questions/7609880
RX_PROPER_NOUNS = re.compile(
    r'''
    (?<!^)                  # Do not match at beginning of string
    (?<![:.?!]\s)           # Ignore at beginning of sentence
    (?<!\{)                 # Ignore words already protected
    \b                      # Word boundary (\w -> \W)
    (\w*[A-Z]\w*)           # Word containing a capital letter
    (\b|$)                  # Word boundary (\w -> \W)
    (?!\})                  # Ignore words already protected
    ''',
    re.X,
)


class _Raw(str):
    """A raw BibTeX string (that is, a macro)"""


def get_journal_initials(journal):
    if isinstance(journal, _Raw):
        journal = JOURNAL_MACRO_TO_NAME[journal]
    return JOURNAL_INITIALS.get(journal, ''.join(re.findall('[A-Z]', journal)))


def normalize_name(name):
    """Normalize the given `name` as `Last, Jr, First`."""
    parts = splitname(name)
    normalized_name = " ".join(parts["von"]) + " ".join(parts["last"])
    if len(parts["jr"]) > 0:
        normalized_name += ", " + " ".join(parts["jr"])
    normalized_name += ", " + " ".join(parts["first"])
    return normalized_name


def get_citekey(first_author, journal, year):
    """Derive a citation key from the given last name, journal, and year.

    The `first_author` should be the last name of the first author, potentially
    with unicode symbols.

    The `journal` should be a journal name (`str`) or abbreviation (`_Raw`),
    i.e. the content of the `journal` bibtex field.

    Lastly, the `year` should be the 4-digit publication years as a string or
    an int.

    Any of the arguments may be None, in which case they are not included
    in the citation key.
    """
    parts = []
    if first_author is not None:
        name = str(first_author)
        name = NAME_UNICODE_MAP.get(name, name)
        parts.append(name)
    if journal is not None:
        parts.append(get_journal_initials(journal))
    if year is not None:
        parts.append(str(year))
    return unidecode("".join(parts))


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


TITLE_LC_WORDS = set(
    # we only need to include words longer than 3 letters
    """from into like near once onto about over than that till upon with when
    """.split()
)


def detect_title_case(title):
    """Heuristically detect if the given `title` string uses title case."""
    lc = 0
    tc = 0
    for word in title.split()[1:]:
        if (
            len(word) > 3
            and word.lower() not in TITLE_LC_WORDS
            and word not in PROTECTED_WORDS
        ):
            if word.capitalize() == word:
                tc += 1
            else:
                lc += 1
    return tc > lc and tc > 2


def protect_strings(s, auto_protect=None):
    if s is not None:
        if auto_protect is None:
            auto_protect = not detect_title_case(s)
        s = s.replace("\n", "\\\\")
        if auto_protect:
            rx_proper_nouns = re.compile(
                r'''
                (?<!^)                  # Do not match at beginning of string
                (?<!\{)                 # Ignore words already protected
                \b                      # Word boundary (\w -> \W)
                (\w*[A-Z]\w{2,})        # Word containing a capital letter
                (\b|$)                  # Word boundary (\w -> \W)
                (?!\})                  # Ignore words already protected
                ''',
                re.X,
            )
            s = RX_PROPER_NOUNS.sub(r'{\1}', s)
        for (rx, repl) in _PROTECTED_WORDS:
            s = rx.sub(repl, s)
    return s
