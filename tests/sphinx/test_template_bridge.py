"""Ensure the Sphinx Template Bridge is replaced and uses the container."""

import pytest
from svcs import Container

from themester.sphinx.models import View
from themester.sphinx.template_bridge import ThemesterBridge

pytestmark = pytest.mark.sphinx("html", testroot="themester-setup")


def test_render_function_view():
    """Test that render gets a View from the container."""

    this_container = {
        View: "FunctionView Result",
    }
    context = {"container": this_container}
    tb = ThemesterBridge()
    result = tb.render("some_template", context)
    assert result == "FunctionView Result"


def test_render_class_view():
    """Test that render gets a class-based View from the container."""

    class CustomView:
        def render(self):
            return "ClassView Result"

    this_container = {
        View: CustomView(),
    }
    context = {"container": this_container}
    tb = ThemesterBridge()
    result = tb.render("some_template", context)
    assert result == "ClassView Result"


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
