# """The event handler for Sphinx's ``html-page-context`` event."""
# from typing import Any
#
# from hopscotch import Registry
# from markupsafe import Markup
# from sphinx.application import Sphinx
#
# from themester.protocols import Resource
# from themester.resources import Site
# from themester.sphinx.models import PageContext
# from themester.sphinx.models import Rellink
# from themester.sphinx.resource import resource_factory
#
#
# def make_page_context(
#     context: dict[str, Any],
#     pagename: str,
#     toc_num_entries: dict[str, int],
#     document_metadata: dict[str, object],
# ) -> PageContext:
#     """Given some Sphinx context information, make a PageContext."""
#     rellinks = tuple(
#         Rellink(
#             pagename=link[0],
#             link_text=link[3],
#             title=link[1],
#             accesskey=link[2],
#         )
#         for link in context.get("rellinks")
#     )
#     # TODO Make this into a service
#     display_toc = (
#         toc_num_entries[pagename] > 1 if "pagename" in toc_num_entries else False
#     )
#     ccf = context.get("css_files")
#     jcf = context.get("css_files")
#     css_files = tuple(ccf) if ccf else tuple()
#     js_files = tuple(jcf) if jcf else tuple()
#     page_context = PageContext(
#         body=Markup(context.get("body", "")),
#         css_files=css_files,
#         display_toc=display_toc,
#         js_files=js_files,
#         meta=document_metadata,
#         metatags=context.get("metatags"),
#         next=context.get("next"),
#         page_source_suffix=context.get("page_source_suffix"),
#         pagename=pagename,
#         pathto=context.get("pathto"),
#         prev=context.get("prev"),
#         sourcename=context.get("sourcename"),
#         rellinks=rellinks,
#         title=context.get("title"),
#         toc=Markup(context.get("toc")),
#         toctree=context.get("toctree"),
#     )
#     return page_context
#
#
# def setup(
#     app: Sphinx,
#     pagename: str,
#     templatename: str,
#     context,
#     doctree,
# ) -> None:
#     """Store a resource-bound container in Sphinx context."""
#     # Make a per-request registry
#     site_registry: Registry = getattr(app, "site_registry")  # noqa: B009
#     context_registry = Registry(parent=site_registry)
#     context["context_registry"] = context_registry
#
#     # Make a PageContext and put it in this registry
#     page_context = make_page_context(
#         context=context,
#         pagename=pagename,
#         toc_num_entries=app.env.toc_num_entries,
#         document_metadata=app.env.metadata[pagename],
#     )
#     context_registry.register(page_context)
#
#     # Make a resource and put it in the registry
#     site = site_registry.get(Site)
#     resource = resource_factory(site, page_context)
#     context_registry.register(resource, kind=Resource)
