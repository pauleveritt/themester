from __future__ import annotations

from viewdom import VDOM


class Resource:
    """A location-aware node in the resource tree."""

    name: str | None
    parent: Resource | None
    title: str | None


class View:
    """A callable that renders to a VDOM."""

    def __call__(self) -> VDOM:
        raise NotImplementedError


class Config:
    """A marker class for configuration information."""

    pass
