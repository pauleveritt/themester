"""Services for the html-page-context Sphinx event."""

from typing import Any

from markupsafe import Markup
from sphinx.addnodes import document
from sphinx.application import (
    Sphinx,
)
from svcs import Container

from themester.sphinx.models import PageContext, Rellink


def make_page_context(
    context: dict[str, Any],
    pagename: str,
    templatename: str,
    toc_num_entries: dict[str, int],
    document_metadata: dict[str, object],
) -> PageContext:
    """Given some Sphinx context information, make a PageContext."""
    rellinks = tuple(
        Rellink(
            pagename=link[0],
            link_text=link[3],
            title=link[1],
            accesskey=link[2],
        )
        for link in context.get("rellinks")
    )

    display_toc = (
        toc_num_entries[pagename] > 1 if "pagename" in toc_num_entries else False
    )
    ccf = context.get("css_files")
    jcf = context.get("css_files")
    # TODO Convert these to Path
    css_files = tuple(ccf) if ccf else ()
    js_files = tuple(jcf) if jcf else ()
    page_context = PageContext(
        body=Markup(context.get("body", "")),
        css_files=css_files,
        display_toc=display_toc,
        js_files=js_files,
        meta=document_metadata,
        metatags=context.get("metatags"),
        next=context.get("next"),
        page_source_suffix=context.get("page_source_suffix"),
        pagename=pagename,
        pathto=context.get("pathto"),
        prev=context.get("prev"),
        sourcename=context.get("sourcename"),
        templatename=templatename,
        rellinks=rellinks,
        title=context.get("title"),
        toc=Markup(context.get("toc")),
        toctree=context.get("toctree"),
    )
    return page_context


def setup(
    app: Sphinx,
    pagename: str,
    templatename: str,
    context,
    doctree,
) -> None:
    """Handle Sphinx's per-page html-page-context event."""

    # Make a per-request container and put in context and app.
    site_registry = getattr(app, "site_registry")
    container = Container(registry=site_registry)
    context["container"] = container
    app.env.current_document["container"] = container

    # Start pulling pieces out of the page context that we might want
    # as isolated services in svcs.
    container.register_local_value(document, doctree)

    # Put the page context in the registry
    page_context = make_page_context(
        context=context,
        pagename=pagename,
        templatename=templatename,
        toc_num_entries=app.env.toc_num_entries,
        document_metadata=app.env.metadata[pagename],
    )
    container.register_local_value(PageContext, page_context)
