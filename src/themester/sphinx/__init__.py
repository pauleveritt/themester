"""Sphinx adapters for Themester."""

from sphinx.application import Sphinx

from . import builder_finished
from . import builder_init
from . import html_page_context


def setup(app: Sphinx) -> None:
    """The Sphinx setup function."""
    app.config.template_bridge = "themester.sphinx.template_bridge.ThemesterBridge"

    # app.connect("builder-inited", builder_init.setup)
    # app.connect("html-page-context", html_page_context.setup)
    # app.connect("build-finished", builder_finished.setup)
