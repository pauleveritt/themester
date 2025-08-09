"""Make sure the top-level __init__ does as expected."""

from typing import TypedDict

import themester


def test_importable() -> None:
    """Can we import the package?"""
    assert themester
