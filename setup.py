#!/usr/bin/env python
"""The setup script."""
import sys

from setuptools import find_packages, setup


def get_version(filename):
    """Extract the package version"""
    with open(filename, encoding='utf8') as in_fh:
        for line in in_fh:
            if line.startswith('__version__'):
                return line.split('=')[1].strip()[1:-1]
    raise ValueError("Cannot extract version from %s" % filename)


with open('README.md', encoding='utf8') as readme_file:
    README = readme_file.read()

try:
    with open('HISTORY.md', encoding='utf8') as history_file:
        HISTORY = history_file.read()
except OSError:
    HISTORY = ''

# requirements for use
requirements = [
    'click',
    'habanero',
]

# requirements for development (testing, generating docs)
dev_requirements = [
    'black',
    'coverage',
    'coveralls',
    'flake8',
    'gitpython',
    'isort',
    'ipython',
    'pre-commit',
    'pdbpp',
    'pylint',
    'pytest',
    'pytest-cov',
    'pytest-xdist',
    'twine',
    'wheel',
]

VERSION = get_version('./src/getbibtex/__init__.py')

setup(
    author="Michael Goerz",
    author_email='mail@michaelgoerz.net',
    description=(
        "A script for getting a BibTeX entry from a URL, DOI, or arXiv ID"
    ),
    python_requires='>=3.8',
    install_requires=requirements,
    extras_require={'dev': dev_requirements},
    license="MIT license",
    long_description=README + '\n\n' + HISTORY,
    long_description_content_type='text/markdown',
    include_package_data=True,
    keywords='getbibtex',
    name='getbibtex',
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    entry_points='''
        [console_scripts]
        getbibtex=getbibtex:main
    ''',
    url='https://github.com/goerz/getbibtex',
    version=VERSION,
    zip_safe=False,
)
