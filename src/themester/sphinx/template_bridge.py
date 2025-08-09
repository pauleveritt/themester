"""Replace the built-in Jinja2 template bridge with Themester."""

from typing import Callable

from sphinx.jinja2glue import BuiltinTemplateLoader
from svcs import Container
from svcs.exceptions import ServiceNotFoundError

from themester.protocols import View


class ThemesterBridge(BuiltinTemplateLoader):
    """Replace the built-in Sphinx template bridge."""

    def render(self, template_or_viewpage: str | Callable, context: dict) -> str:
        """Get a view and render it to a stringable."""

        # The Sphinx html-page-context event makes a svcs.Container for each
        # "request" and stashes this in the Sphinx context object.
        # TODO Adam Make the container first class, rather than smuggling in
        #   via html page context. Should also span further than HTML.
        container: Container = context["container"]

        # Get the correct view from the container and render it.
        # TODO People are going to want alternative policies so make this
        #   a pluggable factory in the registry.
        try:
            view = container.get(View)
        except ServiceNotFoundError:
            # Fall back to regular Sphinx-Jinja rendering
            return super(ThemesterBridge, self).render(template_or_viewpage, context)

        # Class-based view vs. function view
        if hasattr(view, "render"):
            result = view.render()
            return result
        elif type(view) is str:
            result = str(view)
            return result

        # Otherwise, something went wrong.
        raise ValueError("View was neither a string nor a callable")
