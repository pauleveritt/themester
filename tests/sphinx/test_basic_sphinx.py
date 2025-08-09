"""Ensure Sphinx and Sphinx testing work with no Themester."""

import pytest
from sphinx.testing.util import SphinxTestApp

from themester.sphinx import setup

pytestmark = pytest.mark.sphinx("html", testroot="basic-sphinx")


def test_setup(app: SphinxTestApp):
    setup(app)
    assert pytestmark.kwargs["testroot"] == app.config.project


@pytest.mark.parametrize(
    "page",
    [
        "index.html",
    ],
    indirect=True,
)
def test_index(page: str) -> None:
    """Ensure basics are in the page."""
    assert "Hello Sphinx" in page
