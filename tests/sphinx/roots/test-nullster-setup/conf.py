"""Sphinx config file for basic Nullster support."""

from dataclasses import dataclass

from hopscotch import Registry
from viewdom import html
from viewdom import VDOM

from themester.sphinx.models import View

extensions = [
    "themester.sphinx",
    "themester.nullster",
]


@dataclass
class DefaultView:
    """Base view for all pages."""

    def __call__(self) -> VDOM:
        """Generate boilerplate response."""
        return html("<title>Hello World — Python  documentation</title>")


def hopscotch_setup(registry: Registry) -> None:
    """Setup this site."""
    registry.register(DefaultView, kind=View)
