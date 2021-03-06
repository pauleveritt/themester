"""
From ``StandaloneHTMLBuilder.get_doc_context`` which adds keys to
the page context.

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
from typing import Any, Tuple, Optional, Dict, Callable, Iterable

from markupsafe import Markup


@dataclass(frozen=True)
class Rellink:
    pagename: str
    link_text: str
    title: Optional[str] = None
    accesskey: Optional[str] = None


Rellinks = Optional[Tuple[Rellink, ...]]


@dataclass(frozen=True)
class Link:
    """ A connection to another resource """

    link: str
    title: str


Links = Optional[Tuple[Link, ...]]
Meta = Optional[Dict[str, Dict[str, Any]]]


@dataclass(frozen=True)
class PageContext:
    """ Per-page info from the underlying system needed for by layout """

    body: Markup
    css_files: Iterable[str]
    display_toc: bool
    hasdoc: Callable[[str, ], bool]
    js_files: Iterable[str]
    pagename: str
    page_source_suffix: str
    pathto: Callable[[str, ], str]
    sourcename: Optional[str]
    title: str
    toc: Markup
    builder: str = 'html'
    meta: Meta = None
    metatags: str = ''
    next: Optional[Link] = None
    parents: Links = None
    prev: Optional[Link] = None
    rellinks: Rellinks = None
    toctree: Optional[Callable] = None
