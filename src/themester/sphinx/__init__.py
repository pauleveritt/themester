"""Sphinx adapters for Themester."""
from sphinx.application import Sphinx

from . import xxx_html_page_context, xxx_builder_init


def setup(app: Sphinx) -> None:
    """The Sphinx setup function."""
    pass
    # app.config.template_bridge = 'themester.sphinx.template_bridge.ThemesterBridge'
    #
    # app.connect("builder-inited", builder_init.setup)
    # app.connect("html-page-context", html_page_context.setup)
