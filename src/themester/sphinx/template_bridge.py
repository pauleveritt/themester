"""Replace the built-in Jinja2 template bridge with Themester."""
from hopscotch import Registry
from sphinx.jinja2glue import BuiltinTemplateLoader
from viewdom import render

from themester.protocols import Resource, View


class ThemesterBridge(BuiltinTemplateLoader):
    """Replace the built-in Sphinx template bridge."""

    def render(self, template: str, context: dict) -> str:
        """Use viewdom and registry to render a string.

        This is essentially a view layer.
        """
        parent_registry: Registry = context['registry']
        registry = Registry(parent=parent_registry)
        page_context = context['page_context']

        # Get the context and view
        registry.register(page_context)
        context = registry.get(Resource)

        # Now render
        view = registry.get(View, context=context)
        result = render(view(), registry=registry)
        return result
