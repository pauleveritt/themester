from sphinx.application import Sphinx
from venusian import Scanner
from wired import ServiceRegistry

from . import builder_init, builder_finished, inject_page
from .config import SphinxConfig, HTMLConfig
from .factories.resource_factory import resource_factory
from ..nullster.config import NullsterConfig
from ..protocols import Resource
from ..resources import Site
import themester


def setup(app: Sphinx):
    app.config.template_bridge = 'themester.sphinx.template_bridge.ThemesterBridge'

    # Register Sphinx conf.py config values
    app.add_config_value('themester_root', Site(), 'env')
    app.add_config_value('themester_plugins', tuple(), 'env')
    app.add_config_value('theme_config', NullsterConfig(), 'env')
    app.add_config_value('sphinx_config', SphinxConfig(), 'env')
    app.add_config_value('html_config', HTMLConfig(), 'env')

    # Wire up events
    app.connect('builder-inited', builder_init.setup)
    app.connect('html-page-context', inject_page.setup)
    app.connect('build-finished', builder_finished.setup)

    return dict(parallel_read_safe=True)


def wired_setup(
        registry: ServiceRegistry,
        scanner: Scanner,
):
    registry.register_factory(resource_factory, Resource)
    scanner.scan(themester.sphinx)
