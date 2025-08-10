"""Services for the builder-inited Sphinx event."""

from sphinx.application import (
    Sphinx,
    Config as SphinxConfig,
    BuildEnvironment as SphinxBuildEnvironment,
)
from sphinx.builders import Builder


from svcs import Registry

from themester.sphinx.services import svcs_setup as services_setup


def setup(app: Sphinx) -> None:
    """Handle the Sphinx ``builder_init`` event."""
    site_registry = Registry()
    setattr(app, "site_registry", site_registry)  # noqa: B010

    # Add the external data from Sphinx class instances
    site_registry.register_value(Sphinx, app)
    site_registry.register_value(SphinxConfig, app.config)
    site_registry.register_value(SphinxBuildEnvironment, app.env)
    site_registry.register_value(Builder, app.builder)

    # Register the services factories in the registry, not the container.
    services_setup(registry=site_registry)

    # Make a Venusian scanner and put it in the registry. Also, put
    # the registry on the scanner so decorators can get to it and
    # thus get to sphinx_app etc.
    # scanner = Scanner(site_registry=site_registry)
    # site_registry.register_value(Scanner, scanner)

    # Look in conf.py for a `svcs_setup` function
    raw_config = getattr(app.config, "_raw_config")
    svcs_setup = raw_config.get("svcs_setup", None)
    if svcs_setup is not None:
        svcs_setup(site_registry)
