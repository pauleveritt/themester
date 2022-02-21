"""A mostly no-op Themester theme for testing."""
from pathlib import Path

from themester.url import StaticSrc

static_src = StaticSrc(here=Path(__file__), source=Path("static"))
