"""Replace the built-in Jinja2 template bridge with Themester."""

from typing import Callable

from sphinx.jinja2glue import BuiltinTemplateLoader
from svcs import Container

from themester.protocols import View


class TemplateBridge(BuiltinTemplateLoader):
    """Replace the built-in Sphinx template bridge."""

    def render(self, template_or_viewpage: str | Callable, context: dict) -> str:
        """Get a view and render it to a stringable."""

        # The Sphinx html-page-context event makes a svcs.Container for each
        # "request" and stashes this in the Sphinx context object.
        # TODO Adam Make the container first class, rather than smuggling in
        #   via html page context. Should also span further than HTML.
        container: Container = context["container"]

        # Get the correct view from the container and render it.
        view = container.get(View)

        # We might later make it more convenient for Jinja-based views that
        # don't want to set up a Jinja environment and do the render.
        # We could sniff here to see what kind of view it is.
        return view(container=container)
