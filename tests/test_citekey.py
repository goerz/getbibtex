"""Test generating citation keys."""

from getbibtex.bibtex import get_citekey


def test_get_citekey():
    """Test the get_citekey function."""
    key = get_citekey("Imamoğlu", "Phys. Rev. Lett.", 1999)
    assert key == "ImamogluPRL1999"

    # Broken crossref example
    key = get_citekey("Imamog¯lu", "Phys. Rev. Lett.", 1999)
    assert key == "Imamog-luPRL1999"

    key = get_citekey("Sørensen", "Phys. Rev. A", 2018)
    assert key == "SorensenPRA2018"
