"""Sphinx adapters for Themester."""
from sphinx.application import Sphinx


def setup(app: Sphinx) -> None:
    """The Sphinx setup function."""
    app.config.template_bridge = 'themester.sphinx.template_bridge.ThemesterBridge'
