"""Sphinx config file for this test."""

from svcs import Registry, Container

from themester.protocols import View

project = "themester-setup"
extensions = ["themester.sphinx"]


def custom_view(svcs_container: Container):
    return "This is a custom view"


def svcs_setup(registry: Registry):
    """Customize the registry for this site."""

    registry.register_factory(View, custom_view)
