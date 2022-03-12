"""Ensure that Nullster is wired up correctly."""
from typing import cast

import pytest
from hopscotch import Registry

from themester.nullster import NullsterConfig
from themester.nullster.views import IndexView
from themester.protocols import Config
from themester.protocols import View


@pytest.fixture(scope="session")
def nullster_config(nullster_registry: Registry) -> NullsterConfig:
    """Get the Nullster config instance."""
    nullster_config = nullster_registry.get(Config)
    return cast(NullsterConfig, nullster_config)


def test_config(nullster_config: NullsterConfig) -> None:
    """Check the nullster configuration."""
    assert "My Nullster Site" == nullster_config.site_title


def test_index_view(nullster_registry: Registry) -> None:
    """Check the index view."""
    view = cast(IndexView, nullster_registry.get(View))
    assert view.page_title == "View"
    assert view.resource_title == "D1"
