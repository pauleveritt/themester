"""Sphinx adapters for Themester."""
from sphinx.application import Sphinx

from . import html_page_context, builder_init, builder_finished


def setup(app: Sphinx) -> None:
    """The Sphinx setup function."""
    app.config.template_bridge = 'themester.sphinx.template_bridge.ThemesterBridge'

    app.connect("builder-inited", builder_init.setup)
    app.connect("html-page-context", html_page_context.setup)
    app.connect('build-finished', builder_finished.setup)
