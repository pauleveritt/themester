"""Ensure the Sphinx Template Bridge is replaced and uses the container."""

import pytest
from sphinx.testing.util import SphinxTestApp
from svcs import Container

from themester.sphinx.template_bridge import ThemesterBridge
from themester.protocols import View

pytestmark = pytest.mark.sphinx("html", testroot="themester-setup")


def test_render():
    """Test that render gets a View from the container."""

    def get_view(container: Container) -> str:
        return "Some View Result"

    this_container = {
        View: get_view,
    }
    context = {"container": this_container}
    tb = ThemesterBridge()
    result = tb.render("some_template", context)
    assert result == "Some View Result"


def test_no_container():
    """Throw an exception when the context has no container.."""

    # Missing the "container"
    context = {}
    tb = ThemesterBridge()
    with pytest.raises(KeyError):
        tb.render("some_template", context)


@pytest.mark.parametrize(
    "page",
    [
        "index.html",
    ],
    indirect=True,
)
def test_no_views(page: str) -> None:
    """When no view is registered, just use the existing Jinja renderer."""
    assert "Hello Themester" in page
