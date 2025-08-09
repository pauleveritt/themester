"""If a Sphinx extension has a svcs_setup function, run it."""

import pytest
from sphinx.testing.util import SphinxTestApp
from svcs import Registry, Container

pytestmark = pytest.mark.sphinx("html", testroot="svcs-setup")


def test_svcs_setup(app: SphinxTestApp):
    """See if testroot conf.py has a customization function."""
    site_registry: Registry = getattr(app, "site_registry")
    container = Container(registry=site_registry)
    fake_windows_error = container.get(IndentationError)
    assert fake_windows_error == "Fake the IndentationError"


@pytest.mark.parametrize(
    "page",
    [
        "index.html",
    ],
    indirect=True,
)
def test_index(app: SphinxTestApp, page: str) -> None:
    """Ensure basics are in the page."""
    assert "Hello svcs" in page
