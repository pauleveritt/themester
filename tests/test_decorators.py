"""Test the custom injectable decorators."""
from dataclasses import dataclass
from typing import cast

from hopscotch import Registry
from hopscotch.operators import context
from viewdom import html

from themester.decorators import view, config
from themester.protocols import View, Config


@dataclass
class SomeCustomer:
    title: str = "Some Customer"


@config()
@dataclass
class SomeConfig:
    title: str = "My Site"


@view()
@dataclass()
class View1:
    title: str = 'View1'

    def __call__(self) -> int:
        return html(f"<p>Hello {self.title}</p>")


@view(context=SomeCustomer)
@dataclass()
class View2:
    customer_title: str = context(attr="title")

    def __call__(self):
        return self.title


def test_view1() -> None:
    """Lookup a registered view."""
    registry = Registry()
    registry.scan()
    result = cast(View1, registry.get(View))
    assert "View1" == result.title


def test_view2() -> None:
    """Lookup a registered view for a context."""
    registry = Registry(context=SomeCustomer())
    registry.scan()
    result = cast(View2, registry.get(View))
    assert "Some Customer" == result.customer_title


def test_config() -> None:
    """Lookup a registered configuration."""
    registry = Registry()
    registry.scan()
    result = cast(SomeConfig, registry.get(Config))
    assert "My Site" == result.title

