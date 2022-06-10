"""Test auto-protection of titles"""

from getbibtex.bibtex import detect_title_case, protect_strings


def test_protect_strings():
    """Test the `protect_strings` function."""

    title = "Quantum Optimal Control via Semi-Automatic Differentiation"
    title_ = (
        "Quantum {Optimal} {Control} via {Semi}-{Automatic} {Differentiation}"
    )
    assert detect_title_case(title)
    assert protect_strings(title) == title
    assert protect_strings(title, auto_protect=False) == title
    assert protect_strings(title, auto_protect=True) == title_

    title = "Atomic Schrödinger cat states"
    title_ = "Atomic {Schrödinger} cat states"
    assert not detect_title_case(title)
    assert protect_strings(title) == title_
    assert protect_strings(title, auto_protect=True) == title_
    assert protect_strings(title, auto_protect=False) == title_
