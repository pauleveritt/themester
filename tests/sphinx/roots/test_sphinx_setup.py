"""Integration test for Sphinx themester with nullster theme."""

import pytest

pytestmark = pytest.mark.sphinx("html", testroot="sphinx-setup")


@pytest.mark.parametrize(
    "page",
    [
        "index.html",
    ],
    indirect=True,
)
class TestNullsterIndex:
    def test_index(self, page) -> None:
        """Ensure basics are in the page."""
        assert "Hello World — Python  documentation" == page.select_one("title").text
