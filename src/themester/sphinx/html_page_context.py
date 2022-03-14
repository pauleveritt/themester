"""The event handler for Sphinx's ``html-page-context` event."""
from typing import Any

from markupsafe import Markup

from themester.sphinx.models import PageContext, Link, Rellink


def make_page_context(
    context: dict[str, Any],
    pagename: str,
    toc_num_entries: dict[str, int],
    document_metadata: dict[str, object],
) -> PageContext:
    """ Given some Sphinx context information, make a PageContext """
    rellinks = tuple([
        Rellink(
            pagename=link[0],
            link_text=link[3],
            title=link[1],
            accesskey=link[2],
        )
        for link in context.get('rellinks')
    ])
    # TODO Make this into a service
    display_toc = toc_num_entries[pagename] > 1 if 'pagename' in toc_num_entries else False
    ccf = context.get('css_files')
    jcf = context.get('css_files')
    css_files = tuple(ccf) if ccf else tuple()
    js_files = tuple(jcf) if jcf else tuple()
    page_context = PageContext(
        body=Markup(context.get('body', '')),
        css_files=css_files,
        display_toc=display_toc,
        js_files=js_files,
        meta=document_metadata,
        metatags=context.get('metatags'),
        next=context.get('next'),
        page_source_suffix=context.get('page_source_suffix'),
        pagename=pagename,
        pathto=context.get('pathto'),
        prev=context.get('prev'),
        sourcename=context.get('sourcename'),
        rellinks=rellinks,
        title=context.get('title'),
        toc=Markup(context.get('toc')),
        toctree=context.get('toctree'),
    )
    return page_context


def setup(app, pagename, templatename, context, doctree):
    """ Store a resource-bound container in Sphinx context """

    # Make a container and put some Sphinx stuff in it
    registry: InjectorRegistry = getattr(app, 'injector_registry')
    context['injector_registry'] = registry

    # Make a temporary container to get the resource
    temp_container = registry.create_injectable_container()
    temp_container.register_singleton(context, PageContext)
    resource = temp_container.get(Resource)

    # Now make a container with the resource as the context
    container = registry.create_injectable_container(context=resource)
    context['injector_container'] = container

    # Put some things in that container

    # Might was well put the Sphinx build environment in
    env: BuildEnvironment = app.env
    container.register_singleton(env, BuildEnvironment)

    # Let's put the resource in as a singleton, no need to do the
    # lookup again.
    container.register_singleton(resource, Resource)

    # Construct a PageContext from the data Sphinx packed into the
    # html-page-context. Doing so lets us have stronger typing than
    # just dumping it in as-is.
    context['page_context'] = make_page_context(
        context=context,
        pagename=pagename,
        toc_num_entries=env.toc_num_entries,
        document_metadata=env.metadata[pagename],
    )
