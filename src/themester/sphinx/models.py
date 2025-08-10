"""From ``StandaloneHTMLBuilder.get_doc_context`` which adds keys to the page context.

The Sphinx adapter should register_singleton one of these into the
container.

Information from the underlying system about the current page.

In general we want to rely on a resource tree for data about the
currently-rendering "page". But in some systems, like Sphinx, the
framework provides some important computation.

This service collects all the data that themabaster needs -- i.e.
the contract -- for the current "page context".
"""

from dataclasses import dataclass
from typing import Any, Iterable
from typing import Callable
from typing import Protocol

from markupsafe import Markup
from svcs import Container


@dataclass(frozen=True)
class Link:
    """A connection to another resource."""

    link: str
    title: str


@dataclass(frozen=True)
class Rellink:
    """A Sphinx rellink."""

    pagename: str
    link_text: str
    title: str | None = None
    accesskey: str | None = None


Links = tuple[Link, ...] | None
Rellinks = tuple[Rellink, ...] | None
Meta = dict[str, dict[str, Any]] | None


@dataclass(frozen=True)
class PageContext:
    """Per-page info from the underlying system needed by layout."""

    body: Markup
    css_files: Any
    display_toc: bool
    js_files: Any
    pagename: str
    page_source_suffix: str
    pathto: Callable[
        [
            str,
        ],
        str,
    ]
    sourcename: str | None
    title: str
    toc: Markup
    builder: str = "html"
    meta: Meta = None
    metatags: str = ""
    next: Link | None = None
    parents: Links = None
    prev: Link | None = None
    rellinks: Rellinks = None
    toctree: object | None = None


class FunctionView(Protocol):
    """Protocol for callables that render views into stringables."""

    def __call__(self, *, svcs_container: Container) -> str:
        """Use the container to make a string."""
        ...


class _FunctionView(Protocol):
    def __call__(self, svcs_container: Container) -> str: ...


class _ClassView(Protocol):
    def __init__(self, svcs_container: Container): ...

    def render(self) -> str: ...


View = _FunctionView | _ClassView


@dataclass(frozen=True)
class PageContext:
    """Per-page info from the underlying system needed by layout."""

    body: object
    css_files: Iterable
    display_toc: bool
    js_files: Iterable
    pagename: str
    page_source_suffix: str
    pathto: Callable[
        [
            str,
        ],
        str,
    ]
    sourcename: str | None
    templatename: str
    title: str
    toc: object
    builder: str = "html"
    meta: object = None
    metatags: str = ""
    next: object | None = None
    parents: object = None
    prev: object | None = None
    rellinks: object = None
    toctree: object | None = None
