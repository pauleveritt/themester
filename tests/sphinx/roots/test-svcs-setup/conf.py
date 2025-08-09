"""Sphinx config file for this test."""

from svcs import Registry

project = "themester-setup"
extensions = ["themester.sphinx"]


def svcs_setup(registry: Registry):
    """Customize the registry for this site."""

    # We need to register a value for a type, so we can later look up
    # a value we set here in the setup. Let's hijack the IndentationError
    # type.
    registry.register_value(IndentationError, "Fake the IndentationError")
