# getbibtex

[![Source code on Github](https://img.shields.io/badge/goerz-getbibtex-blue.svg?logo=github)][Github]
[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

A script for getting a BibTeX entry from a URL, DOI, or arXiv ID.

For example,

```
$ getbibtex https://scipost.org/10.21468/SciPostPhys.7.6.080
@article{GoerzSPP2019,
    Author = {Goerz, Michael and Basilewitsch, Daniel and Gago-Encinas, Fernando and Krauss, Matthias G. and Horn, Karl P. and Reich, Daniel M. and Koch, Christiane},
    Title = {Krotov: A {Python} implementation of {Krotov}'s method for quantum optimal  control},
    Journal = spp,
    Year = {2019},
    Doi = {10.21468/scipostphys.7.6.080},
    Pages = {080},
    Volume = {7},
    Number = {6},
}
```

The script is very opinionated:

* The citation key is `AuthorJNLyear` where `Author` is an ASCII version of the first author's last name, `JNL` is an abbreviation for the journal in all caps, e.g. `PRL` for [Phys. Rev. Lett.](https://journals.aps.org/prl/), and `year` is the four-digit year in which the article was published. For unpublished [arXiv](https://arxiv.org) articles, the citation key is `AuthorArXivID`, e.g. `Goerz2205.15044` for [arXiv:2205.15044](https://arxiv.org/abs/2205.15044).

* For [known journals](https://github.com/goerz/getbibtex/blob/master/src/getbibtex/journalnames.py), macro names are used exclusively, e.g. `prl` for `Phys. Rev. Lett.` This is to ensure consistent use of [ISO 4](https://en.wikipedia.org/wiki/ISO_4) [journal abbreviations](https://www.cas.org/support/documentation/references/corejournals).

* Full unicode is used in the body of the entry, e.g. for author names. Modern LaTeX seems to handle this just fine, despite claims that `bibtex` is ascii-only.

* All entries have a `Doi` or `Url` field. This is so that with [Revtex](https://journals.aps.org/revtex) and other recent bibliographic styles, all entries in the bibliography will be properly linked.

* Entries are indented with four spaces (no tabs), with every field ending in a comma and the final `}` on a separate line

* There are no non-essential fields in the entry. For examples, articles do not include `month`, `publisher`, `numpages`, a page range, or redundant URLs (all of which are frequently present in publisher-provided bibtex entries). We only keep the feels necessary to render perfectly with [Revtex](https://journals.aps.org/revtex)

Since this is a tool for my own personal usage (or for people who want to adopt my citation style), these features are non-negotiable and I will not consider pull requests that change these, or even add customization. If you want different behavior, you should fork this repository. For this reason `getbibtex` will also not be released on the [Python Package Index](https://pypi.org) (and I would appreciate if you didn't register a package with that name, either!).

Pull Requests that extend the macros of known journals, fix bugs, or extend the script to additional data sources are welcome.


## Installation

It is recommended that you have [pipx](https://pypa.github.io/pipx/) installed as a prerequisite. Then, to install the latest development version of `getbibtex` from [Github][], run

```
pipx install git+https://github.com/goerz/getbibtex.git
```

This will make the `getbibtex` executable available on your system. Alternatively, you can also use simply `pip` instead of `pipx` if you want to do your own environment management.

Assuming have installed `getbibtex` via `pipx`, run

```
pipx reinstall getbibtex
```

to upgrade to the latest `master` version.


## Usage

Further examples are:

```
$ getbibtex https://arxiv.org/abs/2104.07687
@article{Mueller2104.07687,
    Author = {Müller, Matthias M. and Said, Ressa S. and Jelezko, Fedor and Calarco, Tommaso and Montangero, Simone},
    Title = {One decade of quantum optimal control in the chopped random basis},
    Journal = {arXiv:2104.07687},
    Year = {2021},
    Url = {https://doi.org/10.48550/arXiv.2104.07687},
}
```

```
$ getbibtex 10.22331/q-2022-01-24-629
@article{SilverioQ2022,
    Author = {Silvério, Henrique and Grijalva, Sebastián and Dalyac, Constantin and Leclerc, Lucas and Karalekas, Peter J. and Shammah, Nathan and Beji, Mourad and Henry, Louis-Paul and Henriet, Loïc},
    Title = {Pulser: An open-source package for the design of pulse sequences in programmable neutral-atom arrays},
    Journal = quant,
    Year = {2022},
    Doi = {10.22331/q-2022-01-24-629},
    Pages = {629},
    Volume = {6},
}
```

```
$ getbibtex https://journals.aps.org/pra/abstract/10.1103/PhysRevA.89.032334
@article{MuellerPRA2014,
    Author = {Müller, Matthias M. and Murphy, Michael and Montangero, Simone and Calarco, Tommaso and Grangier, Philippe and Browaeys, Antoine},
    Title = {Implementation of an experimentally feasible controlled-phase gate on two blockaded {Rydberg} atoms},
    Journal = pra,
    Year = {2014},
    Doi = {10.1103/physreva.89.032334},
    Pages = {032334},
    Volume = {89},
    Number = {3},
}
```

Run

```
getbibtex --help
```

in your terminal to see all available options.

[Github]: https://github.com/goerz/getbibtex
