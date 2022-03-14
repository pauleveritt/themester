from dataclasses import dataclass

from hopscotch import Registry
from viewdom import VDOM, html

from themester.decorators import view

extensions = [
    "themester.sphinx",
    "myst_parser"
]


@view()
@dataclass
class DefaultView:
    def __call__(self) -> VDOM:
        """Generate boilerplate response."""
        return html("<title>Hello World — Python  documentation</title>")


def hopscotch_setup(registry: Registry) -> None:
    """Setup this site."""
    registry.scan()
