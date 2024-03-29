"""Test Sphinx's implementation of the resource factory."""
from typing import cast

import pytest

from themester.protocols import Resource
from themester.resources import Document
from themester.sphinx.html_page_context import make_page_context
from themester.sphinx.models import PageContext


@pytest.fixture
def this_page_context() -> PageContext:
    """Provide a fake page context for this test."""
    context = dict(
        parents=tuple(),
        rellinks=tuple(),
        title="Some Page",
    )
    pagename = "somepage"
    toc_num_entries = dict()
    document_metadata = dict()

    pc = make_page_context(context, pagename, toc_num_entries, document_metadata)
    return pc


def test_resource_factory(nullster_registry, this_page_context) -> None:
    """See if the resource factory provides a Document."""
    nullster_registry.register(this_page_context)
    resource = cast(Document, nullster_registry.get(Resource))
    assert "D1" == resource.title
