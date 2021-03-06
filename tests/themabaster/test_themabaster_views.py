from bs4 import BeautifulSoup

from themester.sphinx.models import PageContext
from themester.stories import resource, root
from themester.themabaster.stories import page_context
from themester.utils import render_view


def test_render_root_view(themabaster_registry):
    rendered = render_view(
        themabaster_registry,
        resource=root,
        singletons=((page_context, PageContext),)
    )
    this_html = BeautifulSoup(rendered, 'html.parser')
    title = this_html.select_one('title').text
    assert 'Themester Site - Themester SiteConfig' == title


def test_render_document_view(themabaster_registry):
    rendered = render_view(
        themabaster_registry,
        resource=resource,
        singletons=((page_context, PageContext),)
    )
    this_html = BeautifulSoup(rendered, 'html.parser')
    title = this_html.select_one('title').text
    assert 'D2 - Themester SiteConfig' == title
