"""Services for the builder init Sphinx event."""
from pathlib import PurePosixPath

from hopscotch import Registry
from sphinx.application import Sphinx
from sphinx.config import Config

import themester
from themester import nullster
from themester import sphinx
from themester.url import StaticDest


def setup_registry(sphinx_config: Config) -> Registry:
    """Make a registry that is Themester-aware."""
    # Make a registry, wire up themester, sphinx, then plugins
    # using conf.py ``themester_plugins``
    registry = Registry()
    registry.scan(themester)
    registry.scan(sphinx)
    registry.setup(nullster)

    # themester.sphinx.wired_setup(registry)
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

    return registry


def setup(app: Sphinx):
    """ Handle the Sphinx ``builder_init`` event """

    # Make a registry and store it on the app
    registry = setup_registry(sphinx_config=app.config)
    setattr(app, "hopscotch_registry", registry)

    # Register Sphinx app and Sphinx config instance as singletons
    registry.register(app)
    registry.register(app.config)

    # Sphinx wants _static instead of static
    static_dest = StaticDest(dest=PurePosixPath('_static'))
    registry.register(static_dest)
