"""Services for the builder init Sphinx event."""
from importlib import import_module
from importlib import util
from pathlib import Path
from pathlib import PurePosixPath

from hopscotch import Registry
from sphinx.application import Sphinx
from sphinx.config import Config

import themester
from themester.resources import Site
from themester.url import StaticDest


def run_hopscotch_setup(
    registry: Registry,
    sphinx_config: Config,
):
    """Look for ``hopscotch_setup`` in conf.py and Sphinx extensions."""
    raw_config = getattr(sphinx_config, "_raw_config", False)
    if not raw_config:
        # We are probably using the mock, so skip any processing
        return
    # noinspection PyUnresolvedReferences
    # This nonsense is all because of the registry.scan() and
    # caller_module() stuff in Hopscotch means we can't have more
    # than one conf.py per test run. So for now, no scanning in
    # conf.py.
    conf_filename = raw_config["__file__"]
    parent = Path(conf_filename).parent.name
    spec = util.spec_from_file_location(f"{parent}_conf", conf_filename)
    siteconf_module = util.module_from_spec(spec)
    spec.loader.exec_module(siteconf_module)
    hopsotch_setup = getattr(siteconf_module, "hopscotch_setup", None)
    if hopsotch_setup is not None:
        hopsotch_setup(registry)
    registry.scan(siteconf_module)

    # Make a list of places to look for the ``hopscotch_setup`` function
    extensions = sphinx_config.extensions
    for extension in extensions:
        try:
            target_module = import_module(extension)
            hopsotch_setup = getattr(target_module, "hopscotch_setup", None)
            if hopsotch_setup is not None:
                hopsotch_setup(registry)
        except ImportError:
            # conf.py doesn't have a hopsotch_setup
            pass


def setup(app: Sphinx) -> None:
    """Handle the Sphinx ``builder_init`` event."""
    site_registry = Registry()
    setattr(app, "site_registry", site_registry)  # noqa: B010

    # Add the external data from Sphinx class instances
    site_registry.register(app)
    site_registry.register(app.config)
    site_registry.register(app.env)

    # Load the themester/Sphinx core stuff
    site_registry.setup(themester)

    # Look for hopsotch_setup in extensions
    run_hopscotch_setup(site_registry, app.config)

    # Make an instance of a Site and register it
    site_title = app.config["project"]
    themester_root: Site = getattr(app.config, "themester_root", Site(title=site_title))
    site_registry.register(themester_root)

    # Sphinx wants _static instead of static
    static_dest = StaticDest(dest=PurePosixPath("_static"))
    site_registry.register(static_dest)
