import pytest
from sphinx.application import (
    BuildEnvironment as SphinxBuildEnvironment,
)
from sphinx.application import (
    Config as SphinxConfig,
)
from sphinx.application import (
    Sphinx,
)
from sphinx.testing.util import SphinxTestApp
from svcs import Container, Registry
from venusian import Scanner

pytestmark = pytest.mark.sphinx("html", testroot="themester-setup")


def test_builder_inited(app: SphinxTestApp):
    site_registry: Registry = getattr(app, "site_registry")
    container = Container(registry=site_registry)
    sphinx_app = container.get(Sphinx)
    assert isinstance(sphinx_app, SphinxTestApp)
    sphinx_config = container.get(SphinxConfig)
    assert isinstance(sphinx_config, SphinxConfig)
    sphinx_build_env = container.get(SphinxBuildEnvironment)
    assert isinstance(sphinx_build_env, SphinxBuildEnvironment)
    venusian_scanner = container.get(Scanner)
    assert isinstance(venusian_scanner, Scanner)
    assert getattr(venusian_scanner, "site_registry")
