"""Replace the built-in Jinja2 template bridge with Themester."""
from hopscotch import Registry
from sphinx.jinja2glue import BuiltinTemplateLoader
from viewdom import render

from themester.protocols import View


class ThemesterBridge(BuiltinTemplateLoader):
    """Replace the built-in Sphinx template bridge."""

    def render(self, template: str, context: dict) -> str:
        """Use viewdom and registry to render a string.

        This is essentially a view layer.
        """
        context_registry: Registry = context["context_registry"]

        # Now render
        view = context_registry.get(View)
        result = render(view(), registry=context_registry)
        return result
