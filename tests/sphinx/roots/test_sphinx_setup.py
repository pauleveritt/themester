"""Integration test for Sphinx themester with no theme."""
import pytest
from bs4 import BeautifulSoup

pytestmark = pytest.mark.sphinx("html", testroot="sphinx-setup")


@pytest.mark.parametrize(
    "page",
    [
        "index.html",
    ],
    indirect=True,
)
def test_index(page: BeautifulSoup) -> None:
    """Ensure basics are in the page."""
    assert "Hello World — Python  documentation" == page.select_one("title").text
