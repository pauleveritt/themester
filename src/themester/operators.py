"""Custom Themester operators for use in injection."""
from dataclasses import asdict
from dataclasses import dataclass
from pathlib import PurePosixPath
from typing import Any
from typing import Optional

from hopscotch import Registry
from hopscotch.operators import make_field_operator

from themester.resources import Site
from themester.url import find_resource
from themester.url import RelativePath
from themester.url import StaticRelativePath


@dataclass(frozen=True)
class PathTo:
    """Calculate a relative path to a path or resource."""

    lookup_key: Optional[type | PurePosixPath | str] = None

    @staticmethod
    def get_path_function(registry: Registry) -> RelativePath | StaticRelativePath:
        """Isolate this so PathTo and StaticPathTo can share."""
        return registry.get(RelativePath)

    def __call__(
        self,
        registry: Registry,
    ) -> PurePosixPath | str | None:
        """Run the operator."""
        if isinstance(self.lookup_key, str):
            # Make a PurePosixPath then look up
            site = registry.get(Site)
            target = find_resource(site, PurePosixPath(self.lookup_key))
        elif isinstance(self.lookup_key, PurePosixPath):
            # Get the resource from the root and make it the target
            site = registry.get(Site)
            target = find_resource(site, self.lookup_key)
        elif self.lookup_key is not None:
            # We were passed something to go look up
            target = registry.get(self.lookup_key)
        else:
            return None

        relative_path = self.get_path_function(registry)
        return relative_path(target)


path_to = make_field_operator(PathTo)


@dataclass(frozen=True)
class StaticPathTo(PathTo):
    """Calculate a path to a static asset."""

    @staticmethod
    def get_path_function(registry: Registry) -> StaticRelativePath:
        """Isolate this so PathTo and StaticPathTo can share."""
        return registry.get(StaticRelativePath)


static_path_to = make_field_operator(StaticPathTo)


@dataclass(frozen=True)
class AsDict:
    """Convert a dataclass to a dict for use as splat props."""

    lookup_type: Any

    def __call__(
        self,
        registry: Registry,
    ) -> dict[str, Any]:
        """Get the instance from the registry, convert to dict."""
        value = registry.get(self.lookup_type)
        return asdict(value)
