"""Integration test for Sphinx with Nullster."""
import pytest
from bs4 import BeautifulSoup

pytestmark = pytest.mark.sphinx("html", testroot="nullster-setup")


@pytest.mark.parametrize(
    "page",
    [
        "index.html",
    ],
    indirect=True,
)
def test_index(page: BeautifulSoup) -> None:
    """Ensure basics are in the page."""
    assert "Hello World - View" == page.select_one("title").text


@pytest.mark.parametrize(
    "page",
    [
        "_static/nullster.css",
    ],
    indirect=True,
)
def test_nullster_static(page: BeautifulSoup) -> None:
    """Did CSS get copied to output directory?"""
    assert "body {\n}\n" == str(page)
