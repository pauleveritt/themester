"""Ensure that Nullster is wired up correctly."""
from typing import cast

import pytest
from hopscotch import Registry

from themester.nullster import NullsterConfig
from themester.protocols import Config


@pytest.fixture(scope="session")
def nullster_config(nullster_registry: Registry) -> NullsterConfig:
    """Get the Nullster config instance."""
    nullster_config = nullster_registry.get(Config)
    return cast(NullsterConfig, nullster_config)


def test_config(nullster_config: NullsterConfig) -> None:
    """Check the nullster configuration."""
    assert "My Nullster Site" == nullster_config.site_title
