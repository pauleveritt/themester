"""Reusable PEP 544 protocols."""

from typing import Protocol

from svcs import Container


class FunctionView(Protocol):
    """Protocol for callables that render views into stringables."""

    def __call__(self, *, svcs_container: Container) -> str:
        """Use the container to make a string."""
        ...


class _FunctionView(Protocol):
    def __call__(self, svcs_container: Container) -> str: ...


class _ClassView(Protocol):
    def __init__(self, svcs_container: Container): ...

    def render(self) -> str: ...


View = _FunctionView | _ClassView
