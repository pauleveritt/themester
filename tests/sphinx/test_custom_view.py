"""Register a custom view for the template bridge."""

import pytest
from sphinx.testing.util import SphinxTestApp
from svcs import Registry, Container

from themester.protocols import View

pytestmark = pytest.mark.sphinx("html", testroot="custom-view")


def test_custom_view(app: SphinxTestApp):
    """Make sure the container has the view configured in conf.py."""
    site_registry: Registry = getattr(app, "site_registry")
    container = Container(registry=site_registry)
    this_view = container.get(View)
    assert this_view == "This is a custom view"


@pytest.mark.parametrize(
    "page",
    [
        "index.html",
    ],
    indirect=True,
)
def test_index(app: SphinxTestApp, page: str) -> None:
    """Ensure basics are in the page."""
    assert "This is a custom view" in page
