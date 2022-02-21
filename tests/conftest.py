from typing import cast

import pytest
from hopscotch import Registry
from markupsafe import Markup

from themester import url
from themester.protocols import Resource
from themester.resources import Document
from themester.resources import Folder
from themester.resources import Site


@pytest.fixture(scope="session")
def site() -> Site:
    s = Site(title="Themester Site")
    f1 = Folder(name="f1", parent=s, title="F1")
    s["f1"] = f1
    d1 = Document(name="d1", parent=s, title="D1")
    s["d1"] = d1  # type: ignore
    body = Markup("<p>This is <em>great</em>.</p>")
    d2 = Document(name="d2", parent=f1, body=body, title="D2")
    f1["d2"] = d2
    f3 = Folder(name="f3", parent=f1, title="F3")
    f1["f3"] = f3
    d3 = Document(name="d3", parent=f3, title="D3")
    f3["d3"] = d3

    return s


@pytest.fixture(scope="session")
def registry(site: Site) -> Registry:
    r = Registry()
    r.register(site)
    r.scan(url)
    f1 = cast(dict[str, Resource], site["f1"])
    r.register(f1["d2"], kind=Resource)
    return r
