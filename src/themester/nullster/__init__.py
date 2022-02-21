"""A mostly no-op Themester theme for testing."""
from pathlib import Path

from themester.url import StaticSrc

static_src = StaticSrc(here=__file__, source=Path("static"))
