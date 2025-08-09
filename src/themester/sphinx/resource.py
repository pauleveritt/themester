# """Resource factory for Sphinx content."""
# from themester.protocols import Resource
# from themester.resources import Document
# from themester.resources import Site
# from themester.sphinx.models import PageContext
#
#
# def resource_factory(
#     root: Site,
#     page_context: PageContext,
# ) -> Resource | None:
#     """Use info from Sphinx to get a resource for the current page."""
#     # Is this the genindex?
#     # TODO Put this back in place
#     if page_context.pagename in ["genindex", "search"]:
#         return Document(
#             name=page_context.pagename, parent=root, title=page_context.pagename
#         )
#     # Extract what's needed and make a resource
#     document_metadata: dict[str, object] | None = getattr(page_context, "meta", None)
#     if document_metadata is None:
#         return None
#     this_rtype = document_metadata.get("type", "document")
#     if this_rtype is None:
#         return None
#     resource = (
#         root
#         if this_rtype == "homepage"
#         else Document(
#             name=page_context.pagename,
#             parent=root,
#             body=page_context.body,
#             title=page_context.title,
#         )
#     )
#     return resource
