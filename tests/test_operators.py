"""Test the custom operators in Themester."""
from dataclasses import dataclass
from pathlib import PurePosixPath

import pytest
from hopscotch import Registry
from hopscotch import injectable

from themester.operators import AsDict, static_path_to
from themester.operators import PathTo
from themester.operators import StaticPathTo
from themester.operators import path_to
from themester.protocols import Resource
from themester.resources import Site


def test_pathto_setup() -> None:
    """Correctly construct a PathTo operator."""
    lookup_key = PurePosixPath("/doc1")
    this_path_to = PathTo(lookup_key)
    assert lookup_key == this_path_to.lookup_key


def test_pathto_bad_path(site_registry: Registry) -> None:
    """Trying to use lookup something that does not exist."""
    this_path_to = PathTo("/bogus")
    with pytest.raises(KeyError):
        this_path_to(site_registry)


def test_pathto_good_path(site_registry: Registry) -> None:
    """Get a relative path for a resource at a PurePosixPath."""
    this_path_to = PathTo("/f1/d2")
    result = this_path_to(site_registry)
    if isinstance(result, PurePosixPath):
        assert "d2.html" == result.name


@injectable()
@dataclass
class Target:
    """Injectable to test path_to field operator."""
    this_path: PurePosixPath = path_to(PurePosixPath("/f1/d2"))
    this_static_path: PurePosixPath = static_path_to(PurePosixPath("/f1/d2"))


def test_pathto_field(nullster_registry: Registry, site: Site) -> None:
    """See if the pathto field helper for dataclass works."""
    nullster_registry.scan()
    target = nullster_registry.get(Target)
    assert PurePosixPath("f1/d2.html") == target.this_path


def test_staticpathto_setup() -> None:
    """Correctly construct a StaticPathTo operator."""
    lookup_key = PurePosixPath("/doc1")
    path_to = StaticPathTo(lookup_key)
    assert lookup_key == path_to.lookup_key


def test_staticpathto_field(nullster_registry: Registry, site: Site) -> None:
    """See if the staticathto field helper for dataclass works."""
    nullster_registry.scan()
    target = nullster_registry.get(Target)
    assert PurePosixPath("/f1/d2") == target.this_static_path


def test_asdict_setup(site_registry: Registry) -> None:
    """Construct an AsDict operator."""
    as_dict = AsDict(Resource)
    assert Resource is as_dict.lookup_type


def test_asdict_lookup(site_registry: Registry) -> None:
    """Convert the registry's ``Resource`` to a dictionary.."""
    as_dict = AsDict(Resource)
    result = as_dict(site_registry)
    assert "D1" == result["title"]
