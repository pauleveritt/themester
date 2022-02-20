"""Make sure the top-level __init__ does as expected."""
import themester


def test_importable() -> None:
    """Can we import the package?"""

    assert themester
