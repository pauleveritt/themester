"""Test fixtures."""

from pathlib import Path
from typing import Any, Generator

import pytest
from sphinx.testing.util import SphinxTestApp
# from svcs import Registry
#
# from themester.resources import Site, Folder, Document

pytest_plugins = ("sphinx.testing.fixtures",)

_TESTS_ROOT = Path(__file__).resolve().parent
_ROOTS_DIR = _TESTS_ROOT / "sphinx" / "roots"


@pytest.fixture(scope="session")
def rootdir() -> Path:
    return _ROOTS_DIR


@pytest.fixture()
def content(app: SphinxTestApp) -> Generator[SphinxTestApp, Any, None]:
    """The content generated from a Sphinx site."""
    app.build()
    yield app


@pytest.fixture()
def page(content: SphinxTestApp, request) -> Generator[Any, Any, None]:
    """Get the text for a page and convert to BeautifulSoup document."""
    pagename = request.param
    yield (content.outdir / pagename).read_text()


# """Test fixtures."""
# import os
# from pathlib import Path
# from shutil import rmtree
#
# import pytest
# from bs4 import BeautifulSoup
from markupsafe import Markup


# from sphinx.testing.path import path
# from sphinx.testing.util import SphinxTestApp
#
# from themester import nullster
# from themester import url
# from themester.protocols import Resource
# from themester.resources import Document
# from themester.resources import Folder
# from themester.resources import Site
#
# class Registry:
#     pass
# pytest_plugins = [
#     "sphinx.testing.fixtures",
# ]
#
#
# @pytest.fixture(scope="session")
# def site() -> Site:
#     """A fixture for a site with some resources in a tree."""
#     s = Site(title="Themester Site")
#     f1 = Folder(name="f1", parent=s, title="F1")
#     s["f1"] = f1
#     d1 = Document(name="d1", parent=s, title="D1")
#     s["d1"] = d1  # type: ignore
#     body = Markup("<p>This is <em>great</em>.</p>")
#     d2 = Document(name="d2", parent=f1, body=body, title="D2")
#     f1["d2"] = d2
#     f3 = Folder(name="f3", parent=f1, title="F3")
#     f1["f3"] = f3
#     d3 = Document(name="d3", parent=f3, title="D3")
#     f3["d3"] = d3
#
#     return s
#
#
# @pytest.fixture
# def site_registry(site: Site) -> Registry:
#     """A fixture for a configured registry."""
#     registry = Registry()
#     registry.register_value(Site, site)
#     r.register(site)
#     r.scan(url)
#     current_resource = site["d1"]
#     r.register(current_resource, kind=Resource)
#     return r
#

#
#
# @pytest.fixture
# def nullster_registry(site_registry: Registry) -> Registry:
#     """A registry configured for the Nullster theme."""
#     r = Registry(parent=site_registry)
#     r.setup(nullster)
#     r.scan(nullster)
#     return r
#
#
# @pytest.fixture(scope="session")
# def remove_sphinx_projects(sphinx_test_tempdir):
#     """Clean up after Sphinx runs."""
#     # Even upon exception, remove any directory from temp area
#     # which looks like a Sphinx project. This ONLY runs once.
#     roots_path = Path(sphinx_test_tempdir)
#     for d in roots_path.iterdir():
#         if d.is_dir():
#             build_dir = Path(d, "_build")
#             if build_dir.exists():
#                 # This directory is a Sphinx project, remove it
#                 rmtree(str(d))
#
#     yield
#
#
# @pytest.fixture()
# def rootdir(remove_sphinx_projects) -> path:
#     """Top of the Sphinx document tree."""
#     roots = path(os.path.dirname(__file__) or ".").abspath() / "sphinx" / "roots"
#     yield roots
#
#
# @pytest.fixture()
# def content(app: SphinxTestApp) -> None:
#     """The content generated from a Sphinx site."""
#     app.build()
#     yield app
#
#
# @pytest.fixture()
# def page(content: SphinxTestApp, request) -> BeautifulSoup:
#     """Get the text for a page and convert to BeautifulSoup document."""
#     pagename = request.param
#     c = (content.outdir / pagename).read_text()
#
#     yield BeautifulSoup(c, "html.parser")
