"""Services for the builder init Sphinx event."""
import sys
from importlib import import_module
from pathlib import PurePosixPath, Path

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
    raw_config = getattr(sphinx_config, '_raw_config', False)
    if not raw_config:
        # We are probably using the mock, so skip any processing
        return
    # noinspection PyUnresolvedReferences
    conf_filename = Path(raw_config['__file__'])
    conf_parent = conf_filename.parent
    sys.path.insert(0, str(conf_parent))

    # Make a list of places to look for the ``hopscotch_setup`` function
    extensions = sphinx_config.extensions
    extensions.insert(0, "conf")
    for extension in extensions:
        try:
            target_module = import_module(extension)
            hopsotch_setup = getattr(target_module, 'hopscotch_setup', None)
            if hopsotch_setup is not None:
                hopsotch_setup(registry)
        except ImportError:
            # conf.py doesn't have a hopsotch_setup
            pass


def setup(app: Sphinx) -> None:
    """Handle the Sphinx ``builder_init`` event."""
    site_registry = Registry()
    setattr(app, "site_registry", site_registry)

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
    themester_root: Site = getattr(app.config, 'themester_root',
                                   Site(title=site_title))
    site_registry.register(themester_root)

    # Sphinx wants _static instead of static
    static_dest = StaticDest(dest=PurePosixPath('_static'))
    site_registry.register(static_dest)
