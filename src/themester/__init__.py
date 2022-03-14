"""Themester."""
from hopscotch import Registry

from themester import url


def hopscotch_setup(registry: Registry) -> None:
    """Setup this package."""
    registry.scan(url)
