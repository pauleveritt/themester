from pathlib import Path
from pathlib import PurePath
from typing import cast

import pytest

from themester.nullster import static_src
from themester.protocols import Resource
from themester.resources import Site
from themester.url import find_resource
from themester.url import normalize
from themester.url import parents
from themester.url import relative
from themester.url import relative_path
from themester.url import RelativePath
from themester.url import resource_path
from themester.url import StaticRelativePath
from themester.url import StaticSrc


@pytest.mark.parametrize(
    "path, expected",
    [
        (PurePath("/"), None),
        (PurePath("/index"), None),
        (PurePath("/f1"), "f1"),
        (PurePath("/f1/"), "f1"),
        (PurePath("/f1/index"), "f1"),
        (PurePath("/d1"), "d1"),
        (PurePath("/d1/"), "d1"),
        (PurePath("/f1/d2"), "d2"),
        (PurePath("/f1/d2/"), "d2"),
        (PurePath("/f1/f3/"), "f3"),
        (PurePath("/f1/f3"), "f3"),
        (PurePath("/f1/f3/index"), "f3"),
        (PurePath("/f1/f3/"), "f3"),
        (PurePath("/f1/f3/d3"), "d3"),
        (PurePath("/f1/f3/d3/"), "d3"),
    ],
)
def test_find_resource(path: PurePath, expected: str, site: Site) -> None:
    """Use the site fixture to see if find_resource logic works."""
    resource = find_resource(site, path)
    assert resource.name == expected


def test_find_resource_missing_slash(site: Site) -> None:
    """Missing slash at path beginning should give ValueError"""

    path = PurePath("f1/XXX")
    with pytest.raises(ValueError) as exc:
        find_resource(site, path)
    expected = 'ResourceLike path "f1/XXX" must start with a slash'
    assert expected == exc.value.args[0]


@pytest.mark.parametrize(
    "path, expected",
    [
        (PurePath("/XXX"), 'No resource at path "/XXX"'),
        (PurePath("/f1/XXX"), 'No resource at path "/f1/XXX"'),
    ],
)
def test_find_resource_failed(path: PurePath, expected: str, site: Site) -> None:
    """Provide a bogus path and get a LookupError."""

    with pytest.raises(KeyError) as exc:
        find_resource(site, path)
    assert expected == exc.value.args[0]


@pytest.mark.parametrize(
    "this_path, expected",
    (
        (PurePath("/"), ()),
        (PurePath("/f1/"), ((None, PurePath("/")),)),
        (PurePath("/d1"), ((None, PurePath("/")),)),
        (
            PurePath("/f1/d2"),
            (
                (None, PurePath("/")),
                ("f1", PurePath("/f1/")),
            ),
        ),
        (
            PurePath("/f1/f3/"),
            (
                (None, PurePath("/")),
                ("f1", PurePath("/f1/")),
            ),
        ),
        (
            PurePath("/f1/f3/d3"),
            (
                (None, PurePath("/")),
                ("f1", PurePath("/f1/")),
                ("f3", PurePath("/f1/f3/")),
            ),
        ),
    ),
)
def test_parents(
    this_path: PurePath,
    expected: tuple[tuple[str, PurePath]],
    site: Site,
) -> None:
    """Ensure the lineage is setup correctly."""
    resource = find_resource(site, this_path)
    results = parents(resource)
    result = tuple((resource.name, resource_path(resource)) for resource in results)
    assert expected == result


@pytest.mark.parametrize(
    "target, expected",
    (
        (PurePath("/"), PurePath("/")),
        (PurePath("/f1"), PurePath("/f1/")),
        (PurePath("/f1/"), PurePath("/f1/")),
        (PurePath("/d1"), PurePath("/d1/")),
        (PurePath("/d1/"), PurePath("/d1/")),
        (PurePath("/f1/d2"), PurePath("/f1/d2/")),
        (PurePath("/f1/d2/"), PurePath("/f1/d2/")),
        (PurePath("/f1/f3"), PurePath("/f1/f3/")),
        (PurePath("/f1/f3/"), PurePath("/f1/f3/")),
        (PurePath("/f1/f3/d3"), PurePath("/f1/f3/d3/")),
        (PurePath("/f1/f3/d3/"), PurePath("/f1/f3/d3/")),
    ),
)
def test_resource_path(target: PurePath, expected: PurePath, site: Site) -> None:
    """Check nested resource paths."""
    r = find_resource(site, target)
    path = resource_path(r)
    assert expected == path


@pytest.mark.parametrize(
    "current, target, expected",
    [
        (PurePath("/index"), PurePath("/index"), PurePath("index")),
        (PurePath("/d1"), PurePath("/d1"), PurePath("d1")),
        (PurePath("/d1/"), PurePath("/d1"), PurePath("d1")),
        (PurePath("/f1/f3/index"), PurePath("/f1/d2"), PurePath("../d2")),
        (PurePath("/f1/f3/d3"), PurePath("/d1"), PurePath("../../d1")),
        (PurePath("/f1/f3/d3"), PurePath("/index"), PurePath("../../index")),
        (PurePath("/f1/f3/d3"), PurePath("/f1/index"), PurePath("../index")),
        (PurePath("/f1/f3/d3"), PurePath("/f1/f3/index"), PurePath("index")),
        (PurePath("/d1"), PurePath("/f1/f3/d3/"), PurePath("f1/f3/d3")),
        (PurePath("/f1/f3/index"), PurePath("/index"), PurePath("../../index")),
        (PurePath("/f1/f3/index"), PurePath("/f1/index"), PurePath("../index")),
        (PurePath("/f1/f3/index"), PurePath("/f1/f3/d3"), PurePath("d3")),
        (PurePath("/index"), PurePath("/d1"), PurePath("d1")),
        (PurePath("/d1"), PurePath("/index"), PurePath("index")),
    ],
)
def test_relative_path(
    current: PurePath,
    target: PurePath,
    expected: PurePath,
) -> None:
    """Check relative paths between a source and a target."""
    result = relative_path(current, target)
    assert expected == result


@pytest.mark.parametrize(
    "current, expected",
    [
        (PurePath("/index"), PurePath("static/css/styles.css")),
        (PurePath("/d1"), PurePath("static/css/styles.css")),
        (PurePath("/f1/index"), PurePath("../static/css/styles.css")),
        (PurePath("/f1/f3/index"), PurePath("../../static/css/styles.css")),
        (PurePath("/f1/f3/d3"), PurePath("../../static/css/styles.css")),
    ],
)
def test_relative_path_static(current: PurePath, expected: PurePath) -> None:
    """Relative paths between two resources, but involving the static path."""
    root_path = PurePath("/")
    target = PurePath("css/styles.css")
    static_prefix = PurePath("static")

    rp = relative_path(current, root_path, static_prefix=static_prefix)
    result = rp / target
    assert expected == result


@pytest.mark.parametrize(
    "current, expected",
    (
        (PurePath("/"), PurePath("/index")),
        (PurePath("/index"), PurePath("/index")),
        ("site", PurePath("/index")),
        ("site", PurePath("/index")),
        ("/f1/d2", PurePath("/f1/d2")),
    ),
)
def test_normalize(current: PurePath | str, expected: PurePath, site: Site) -> None:
    """Test passing resources, paths, and strings."""
    if current == "site":
        path = normalize(cast(Resource, site))
    elif current == "/f1/d2":
        f1 = cast(dict[str, Resource], site["f1"])
        path = normalize(f1["d2"])
    else:
        path = normalize(current)
    assert expected == path


@pytest.mark.parametrize(
    "current, target, static_prefix, suffix, expected",
    (
        (PurePath("/"), PurePath("/"), None, None, PurePath("index")),
        (PurePath("/"), PurePath("/"), None, ".html", PurePath("index.html")),
        (PurePath("/index"), PurePath("/"), None, None, PurePath("index")),
        (PurePath("/"), PurePath("/index"), None, None, PurePath("index")),
        (PurePath("/f1/d2"), PurePath("/d1"), None, None, PurePath("d1")),
        (PurePath("/f1/d2"), PurePath("/d1"), None, ".html", PurePath("d1.html")),
        (
            PurePath("/f1/d2"),
            PurePath("icon.png"),
            PurePath("/tmp"),
            None,
            PurePath("/tmp/icon.png"),
        ),
    ),
)
def test_relative(
    current: PurePath,
    target: PurePath,
    static_prefix: PurePath | None,
    suffix: str | None,
    expected: PurePath,
    site: Site,
) -> None:
    """More of the integrated test."""
    s = cast(Resource, site)
    path = relative(s, target, static_prefix=static_prefix, suffix=suffix)
    assert expected == path


def test_factory_relative_path(site: Site) -> None:
    """Use the registry and a factory to get the path."""
    f1 = cast(dict[str, Resource], site["f1"])
    resource = f1["d2"]
    srp = RelativePath(resource=resource)
    target = PurePath("/foo/bar/baz")
    result = srp(target)
    assert PurePath("../foo/bar/baz.html") == result


def test_factory_static_relative_path(site: Site) -> None:
    from themester import nullster

    this_static_src = StaticSrc(
        here=Path(nullster.__file__),
        source=Path("../src/themester/nullster/static/nullster.css"),
    )
    resource = site["d1"]
    srp = StaticRelativePath(
        resource=cast(Resource, resource),
        static_src=this_static_src,
    )
    target = PurePath("images/favicon.ico")
    result = srp(target)
    assert PurePath("static/images/favicon.ico") == result


def test_here_one_level() -> None:
    this_source = Path(".")  # themabaster/tests/factories
    here = StaticSrc(here=Path(__file__), source=this_source)
    expected = Path(__file__).parent
    assert expected == here.source
    target = Path("../tests/test_url.py")
    result = here(target)
    assert Path("test_url.py") == result


def test_here_two_levels() -> None:
    this_source = Path("..")  # themabaster/tests
    here = StaticSrc(here=Path(__file__), source=this_source)
    expected = Path(__file__).parent.parent
    assert expected == here.source
    target = Path("../tests/test_url.py")
    result = here(target)
    assert Path("tests/test_url.py") == result


def test_here_three_levels() -> None:
    this_source = Path("../..")  # themabaster
    here = StaticSrc(here=Path(__file__), source=this_source)
    expected = Path(__file__).parent.parent.parent
    assert expected == here.source

    target = Path("../../tests/test_url.py")
    result = here(target)
    assert Path("tests/test_url.py") == result


def test_here_themabaster() -> None:
    target = Path("../src/themester/nullster/static/nullster.css")
    result = static_src(target)
    assert Path("nullster.css") == result
