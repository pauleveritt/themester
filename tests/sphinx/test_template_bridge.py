"""Test the template bridge."""
import pytest
from bs4 import BeautifulSoup
from hopscotch import Registry

from themester.sphinx.html_page_context import make_page_context
from themester.sphinx.xxx_models import PageContext
from themester.sphinx.template_bridge import ThemesterBridge


@pytest.fixture
def page_context() -> PageContext:
    """Provide a mocked page context."""
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


def test_page_context(page_context: PageContext) -> None:
    """Ensure fixture works ok."""
    assert "somepage" == page_context.pagename


def test_template_bridge_instance(nullster_registry: Registry) -> None:
    """See if we can make an instance of a TemplateBridge."""
    tb = ThemesterBridge()
    context = dict(
        registry=nullster_registry,
        page_context=page_context,
    )
    rendered = tb.render("", context)
    result = BeautifulSoup(rendered, "html.parser")
    assert "D1 - View" == result.select_one("title").text
