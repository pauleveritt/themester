"""Ensure that Nullster is wired up correctly."""
from typing import cast

import pytest
from bs4 import BeautifulSoup
from hopscotch import Registry
from viewdom import render

from themester.nullster import NullsterConfig
from themester.nullster.views import IndexView
from themester.protocols import Config
from themester.protocols import View


@pytest.fixture
def nullster_config(nullster_registry: Registry) -> NullsterConfig:
    """Get the Nullster config instance."""
    nullster_config = nullster_registry.get(Config)
    return cast(NullsterConfig, nullster_config)


def test_config(nullster_config: NullsterConfig) -> None:
    """Check the nullster configuration."""
    assert "My Nullster Site" == nullster_config.site_title


def test_nullster_registry(nullster_registry: Registry) -> None:
    """Ensure the Nullster registry is wired up correctly."""
    view = nullster_registry.get(View)
    assert isinstance(view, IndexView)


def test_index_view(nullster_registry: Registry) -> None:
    """Check the index view."""
    view = cast(IndexView, nullster_registry.get(View))
    assert view.page_title == "View"
    assert view.resource_title == "D1"
    result = render(view(), registry=nullster_registry)
    page = BeautifulSoup(result, "html.parser")
    assert "D1 - View" == page.select_one("title").text
    assert "static/nullster.css" == page.select_one("link").attrs["href"]
