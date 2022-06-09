# getbibtex

[![Source code on Github](https://img.shields.io/badge/goerz-getbibtex-blue.svg?logo=github)][Github]
[![Tests](https://github.com/goerz/getbibtex/workflows/Tests/badge.svg?branch=master)](https://github.com/goerz/getbibtex/actions?query=workflow%3ATests)
[![Coverage](https://codecov.io/gh/goerz/getbibtex/branch/master/graph/badge.svg)](https://codecov.io/gh/goerz/getbibtex)
[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

A script for getting a BibTeX entry from a URL, DOI, or arXiv ID.

The script is very opinionated:

* The citation key is `AuthorJOURNALyear` where `Author` is an ASCII version of the first author's last name, `JOURNAL` is an abbreviation for the journal in all caps, e.g. `PRL` for [Phys. Rev. Lett.](https://journals.aps.org/prl/), and `year` is the four-digit year in which the article was published. For unpublished [arXiv](https://arxiv.org) articles, the citation key is `AuthorArXivID`, e.g. `Goerz2205.15044` for [arXiv:2205.15044](https://arxiv.org/abs/2205.15044).

* For known journals, macro names are used exclusively

* Full unicode is used in the body of the entry, e.g. for author names. Modern LaTeX seems to handle this just fine, despite claims that `bibtex` is ascii-only.

* All entries have a `Doi` field

* Entries are indented with four spaces (no tabs), with every field ending in a comma and the final `}` on a separate line

* There are no non-essential fields in the entry

Since this is a tool for my own personal usage (or for people who want to adopt my citation style), these features are non-negotiable and I will not consider pull requests that change these, or even add customization. If you want different behavior, you should fork this repository. For this reason `getbibtex` will also not be released on the [Python Package Index](https://pypi.org) (and I would appreciate if you didn't register a package with that name, either!).

PRs that extend the macros of known journals, fix bugs, or extend the script to additional data sources are welcome.


## Installation

It is recommended that you have [pipx](https://pypa.github.io/pipx/) installed as a prerequisite. Then, to install the latest development version of getbibtex from [Github][], run

```
pipx install git+https://github.com/goerz/getbibtex.git
```

This will make the `getbibtex` executable available on your system. Alternatively, you can also use simply `pip` instead of `pipx` if you want to do your own environment management.


## Usage

Run

```
getbibtex --help
```

in your terminal

[Github]: https://github.com/goerz/getbibtex
