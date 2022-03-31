"""Sphinx config file for this test."""
from dataclasses import dataclass
from pathlib import Path

from hopscotch import Registry
from viewdom import VDOM
from viewdom import html

from themester.decorators import view
from themester.url import StaticSrc

extensions = ["themester.sphinx", "myst_parser"]
here = Path(__file__)


@view()
@dataclass
class DefaultView:
    """Fake view for this Sphinx site."""

    def __call__(self) -> VDOM:
        """Generate boilerplate response."""
        return html("<title>Hello World — Python  documentation</title>")


def hopscotch_setup(registry: Registry) -> None:
    """Setup this site."""
    static_src = StaticSrc(here, source=Path("static"))
    registry.register(static_src)
    registry.scan()