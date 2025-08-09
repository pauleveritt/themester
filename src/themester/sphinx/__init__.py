"""Sphinx adapters for Themester."""

from sphinx.application import Sphinx

from themester.sphinx import builder_inited, html_page_context


def setup(app: Sphinx) -> None:
    """The Sphinx setup function."""
    app.config.template_bridge = "themester.sphinx.template_bridge.ThemesterBridge"

    app.connect("builder-inited", builder_inited.setup)
    app.connect("html-page-context", html_page_context.setup)

    # We don't use this for now. Later when we bring back themes in
    # and they need to copy assets.
    # app.connect("build-finished", builder_finished.setup)
