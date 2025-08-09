from typing import NotRequired, TypedDict

import pytest
from sphinx.testing.util import SphinxTestApp
from svcs import Container

from themester.sphinx.html_page_context import setup

pytestmark = pytest.mark.sphinx("html", testroot="themester-setup")


class ContextDict(TypedDict):
    """Sphinx will later provide this."""

    container: NotRequired[Container]


@pytest.fixture
def context() -> ContextDict:
    return {}


def test_html_page_context(app: SphinxTestApp, context: ContextDict) -> None:
    """Extract info from Sphinx to make a PageContext instance."""
    doctree = {}
    setup(app, "pagename", "templatename", context, doctree)
    assert isinstance(app.env.current_document["container"], Container)
    assert isinstance(context["container"], Container)
