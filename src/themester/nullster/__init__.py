"""A mostly no-op Themester theme for testing."""
from dataclasses import dataclass
from pathlib import Path

from hopscotch import Registry

from . import views
from themester.decorators import config
from themester.url import StaticSrc

here = Path(__file__)


@config()
@dataclass
class NullsterConfig:
    """Basic config info for this demo theme."""

    site_title: str = "My Nullster Site"
    # static_dir: str = StaticDest(dest=PurePosixPath("./static/nullster.css"))


def hopscotch_setup(registry: Registry) -> None:
    """Setup this package."""
    static_src = StaticSrc(here, source=Path("static"))
    registry.register(static_src)
    registry.scan(views)
