"""Default implementations of resource protocols."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from markupsafe import Markup

from themester.protocols import Resource


@dataclass
class Site(dict[str, Resource | dict[str, Resource]]):
    """Top-level resource at the root of a site."""

    title: str
    name: None = None
    parent: None = None
    body: Markup | None = None

    def __post_init__(self) -> None:
        """Setup the dict."""
        super().__init__()


@dataclass(frozen=True)
class Folder(dict[str, Any]):
    """A folder in the resource tree."""

    name: str
    parent: Site | Folder
    title: str
    body: Markup | None = None

    def __post_init__(self) -> None:
        """Setup the dict."""
        super().__init__()


@dataclass(frozen=True)
class Document:
    """A leaf in the resource tree."""

    name: str
    parent: Site | Folder
    title: str
    body: Markup | None = None
