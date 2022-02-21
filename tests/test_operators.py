"""Test the custom operators in Themester."""
from pathlib import PurePath

import pytest
from hopscotch import Registry

from themester.operators import AsDict
from themester.operators import PathTo
from themester.operators import StaticPathTo
from themester.protocols import Resource


def test_pathto_setup() -> None:
    """Correctly construct a PathTo operator."""

    lookup_key = PurePath("/doc1")
    path_to = PathTo(lookup_key)
    assert lookup_key == path_to.lookup_key


def test_pathto_bad_path(registry: Registry) -> None:
    """Trying to use lookup something that does not exist."""

    path_to = PathTo("/bogus")
    with pytest.raises(KeyError):
        path_to(registry)


def test_pathto_good_path(registry: Registry) -> None:
    """Get a relative path for a resource at a PurePath."""

    path_to = PathTo("/f1/d2")
    result = path_to(registry)
    if isinstance(result, PurePath):
        assert "d2.html" == result.name


def test_staticpathto_setup() -> None:
    """Correctly construct a StaticPathTo operator."""

    lookup_key = PurePath("/doc1")
    path_to = StaticPathTo(lookup_key)
    assert lookup_key == path_to.lookup_key


def test_asdict_setup(registry: Registry) -> None:
    """Construct an AsDict operator."""

    as_dict = AsDict(Resource)
    assert Resource is as_dict.lookup_type


def test_asdict_lookup(registry: Registry) -> None:
    """Convert the registry's ``Resource`` to a dictionary.."""

    as_dict = AsDict(Resource)
    result = as_dict(registry)
    assert "D2" == result["title"]
