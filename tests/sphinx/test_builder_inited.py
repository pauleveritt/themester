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

from themester.sphinx.services import BuilderConfig, PathTo, RelativeUri, TargetUri

pytestmark = pytest.mark.sphinx("html", testroot="themester-setup")


def test_builder_inited(app: SphinxTestApp):
    site_registry: Registry = getattr(app, "site_registry")
    container = Container(registry=site_registry)
    assert isinstance(container.get(Sphinx), SphinxTestApp)
    assert isinstance(container.get(SphinxConfig), SphinxConfig)
    assert isinstance(container.get(SphinxBuildEnvironment), SphinxBuildEnvironment)
    assert isinstance(container.get(BuilderConfig), BuilderConfig)
    assert isinstance(container.get(PathTo), PathTo)
    assert isinstance(container.get(RelativeUri), RelativeUri)
    assert isinstance(container.get(TargetUri), TargetUri)
    # venusian_scanner = container.get(Scanner)
    # assert isinstance(venusian_scanner, Scanner)
    # assert getattr(venusian_scanner, "site_registry")
