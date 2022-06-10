"""Test regular expressions."""

from getbibtex import RX_ARXIV_NEW, RX_ARXIV_OLD, RX_DOI


def test_rx_doi():
    """Test the regex for finding DOIs."""
    query = r'https://doi.org/10.22331/q-2022-01-24-629'
    match = RX_DOI.search(query)
    assert bool(match) is True


def test_rx_arxiv_new():
    """Test the regex for finding new-style arXiv identifiers."""

    query = r'https://arxiv.org/abs/2205.15044'
    match = RX_ARXIV_NEW.search(query)
    assert bool(match) is True
    assert match.group(1) == "2205.15044"

    query = r'https://doi.org/10.48550/arXiv.2205.15044'
    match = RX_ARXIV_NEW.search(query)
    assert bool(match) is True
    assert match.group(1) == "2205.15044"


def test_rx_arxiv_old():
    """Test the regex for finding old-style arXiv identifiers."""

    query = r'arXiv:cond-mat/0411174v1'
    match = RX_ARXIV_OLD.search(query)
    assert bool(match) is True
    assert match.group(1) == "cond-mat/0411174v1"

    query = r'https://arxiv.org/abs/cond-mat/0411174'
    match = RX_ARXIV_OLD.search(query)
    assert bool(match) is True
    assert match.group(1) == "cond-mat/0411174"
