"""Services for the builder init Sphinx event."""
import sys
from importlib import import_module
from importlib.util import spec_from_file_location, module_from_spec
from pathlib import PurePosixPath, Path

from hopscotch import Registry
from sphinx.application import Sphinx
from sphinx.config import Config

import themester
from themester.url import StaticDest


def setup_registry(sphinx_config: Config) -> Registry:
    """Make a registry that is Themester-aware."""
    # sphinx_extensions: Tuple[str] = sphinx_config.extensions
    # for sphinx_extension in sphinx_extensions:
    #     # If the extension has ``wired_setup``, then call it
    #     target = import_module(sphinx_extension)
    #     wired_setup = getattr(target, 'wired_setup', None)
    #     if wired_setup is not None:
    #         wired_setup(registry)

    # Look for wired_setup in conf.py
    # run_wired_setup(registry, sphinx_config)

    # Wire up site
    # themester_root: Site = getattr(sphinx_config, 'themester_root', None)
    # if themester_root is not None:
    #     # We are customizing the root
    #     registry.register_singleton(themester_root, Root)

    return


def run_hopscotch_setup(
    registry: Registry,
    sphinx_config: Config,
):
    """Look for ``wired_setup`` in conf.py."""
    # Start by adding the path to conf.py to the python path.

    raw_config = getattr(sphinx_config, '_raw_config', False)
    if not raw_config:
        # We are probably using the mock, so skip any processing
        return
    # noinspection PyUnresolvedReferences
    conf_filename = Path(raw_config['__file__'])
    conf_parent = conf_filename.parent
    sys.path.insert(0, str(conf_parent))
    try:
        conf = import_module('conf')
        wired_setup = getattr(conf, 'hopscotch_setup', None)
        if wired_setup is not None:
            wired_setup(registry)
    except ImportError:
        # conf.py doesn't have a wired_setup
        pass


def setup(app: Sphinx) -> None:
    """Handle the Sphinx ``builder_init`` event."""
    site_registry = Registry()
    setattr(app, "site_registry", site_registry)

    # Add the external data in Sphinx
    site_registry.register(app)
    site_registry.register(app.config)
    site_registry.register(app.env)

    # Load the themester core stuff
    site_registry.setup(themester)

    # Look for wired_setup in conf.py
    run_hopscotch_setup(site_registry, app.config)

    # Sphinx wants _static instead of static
    static_dest = StaticDest(dest=PurePosixPath('_static'))
    site_registry.register(static_dest)
