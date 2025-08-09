"""Ensure the Sphinx Template Bridge is replaced and uses the container."""

import pytest
from svcs import Container

from themester.sphinx.template_bridge import TemplateBridge
from themester.protocols import View


def test_render():
    """Test that render gets a View from the container."""

    def get_view(container: Container) -> str:
        return "Some View Result"

    this_container = {
        View: get_view,
    }
    context = {"container": this_container}
    tb = TemplateBridge()
    result = tb.render("some_template", context)
    assert result == "Some View Result"


def test_no_container():
    """Throw an exception when the context has no container.."""

    # Missing the "container"
    context = {}
    tb = TemplateBridge()
    with pytest.raises(KeyError):
        tb.render("some_template", context)
