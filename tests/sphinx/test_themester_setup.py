"""Ensure Themester got registered with Sphinx and put a flag in the registry."""

import pytest
from sphinx.testing.util import SphinxTestApp

pytestmark = pytest.mark.sphinx("html", testroot="themester-setup")


def test_setup(app: SphinxTestApp):
    """Manually configure a Sphinx app with Themester setup."""
    site_registry = getattr(app, "site_registry", None)
    assert site_registry is not None


@pytest.mark.parametrize(
    "page",
    [
        "index.html",
    ],
    indirect=True,
)
def test_index(page: str) -> None:
    """Ensure basics are in the page."""
    assert "Hello Themester" in page
