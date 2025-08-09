"""Reusable PEP 544 protocols."""

from __future__ import annotations

from typing import Protocol

from svcs import Container


class Resource:
    """A location-aware node in the resource tree."""

    name: str | None
    parent: Resource | None
    title: str | None


class FunctionView(Protocol):
    """Protocol for callables that render views into stringables."""

    def __call__(self, *, container: Container) -> str:
        """Use the container to make a string."""
        ...


class View(Protocol):
    """Protocol for callables that render views into stringables."""

    def __call__(self, *, container: Container) -> str:
        """Use the container to make a string."""
        ...

    def render(self) -> str: ...


class Config:
    """A marker for config information across all backends."""

    pass
