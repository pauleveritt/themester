# """Test the custom injectable decorators."""
# from dataclasses import dataclass
# from typing import cast
#
# from hopscotch import Registry
# from hopscotch.operators import context
# from viewdom import html
# from viewdom import VDOM
#
# from themester.decorators import config
# from themester.decorators import view
# from themester.protocols import Config
# from themester.protocols import View
#
#
# @dataclass
# class SomeCustomer:
#     """A unit of data used as a context."""
#
#     title: str = "Some Customer"
#
#
# @config()
# @dataclass
# class SomeConfig:
#     """Basic config info for this site."""
#
#     title: str = "My Site"
#
#
# @view()
# @dataclass()
# class View1:
#     """Default views for all contexts."""
#
#     title: str = "View1"
#
#     def __call__(self) -> VDOM:
#         """Render the view."""
#         return html(f"<p>Hello {self.title}</p>")
#
#
# @view(context=SomeCustomer)
# @dataclass()
# class View2:
#     """An alternative view for a context."""
#
#     customer_title: str = context(attr="title")
#
#     def __call__(self) -> VDOM:
#         """Call the view."""
#         return html(f"<p>Goodbye {self.customer_title}</p>")
#
#
# def test_view1() -> None:
#     """Lookup a registered view."""
#     registry = Registry()
#     registry.scan()
#     result = cast(View1, registry.get(View))
#     assert "View1" == result.title
#
#
# def test_view2() -> None:
#     """Lookup a registered view for a context."""
#     registry = Registry(context=SomeCustomer())
#     registry.scan()
#     result = cast(View2, registry.get(View))
#     assert "Some Customer" == result.customer_title
#
#
# def test_config() -> None:
#     """Lookup a registered configuration."""
#     registry = Registry()
#     registry.scan()
#     result = cast(SomeConfig, registry.get(Config))
#     assert "My Site" == result.title
