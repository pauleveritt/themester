from __future__ import annotations

from typing import Protocol


class ResourceLike(Protocol):
    """A location-aware node in the resource tree."""

    name: str | None
    parent: ResourceLike | None
    title: str | None


#
# class CollectionLike(Protocol):
#     """Folders in the resource tree."""
#
#     def __getitem__(self, key: str) -> ResourceLike:
#         ...
#
#     def __iter__(self) -> Iterable[str]:
#         ...
#
#     def __len__(self) -> int:
#         ...
#
#     def get(self, key: str) -> ResourceLike | None:
#         ...
#
#     def __contains__(self, key):
#         ...
#
#     def keys(self):
#         ...
#
#     def items(self):
#         ...
#
#     def values(self):
#         ...
#
#     def __eq__(self, other):
#         ...
#
#
#
#
# class RootLike(ResourceLike, CollectionLike, Protocol):
#     """The root of the resource tree."""
#
#
# class FolderLike(ResourceLike, CollectionLike, Protocol):
#     """A collection in the resource tree."""
#
#     pass
#
#
# class DocumentLike(ResourceLike, Protocol):
#     """A collection in the resource tree."""
#
#     body: Markup | None
