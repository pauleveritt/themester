"""Test the url and path helper functions."""
from pathlib import Path
from pathlib import PurePosixPath
from typing import cast

import pytest

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
        (PurePosixPath("/"), None),
        (PurePosixPath("/index"), None),
        (PurePosixPath("/f1"), "f1"),
        (PurePosixPath("/f1/"), "f1"),
        (PurePosixPath("/f1/index"), "f1"),
        (PurePosixPath("/d1"), "d1"),
        (PurePosixPath("/d1/"), "d1"),
        (PurePosixPath("/f1/d2"), "d2"),
        (PurePosixPath("/f1/d2/"), "d2"),
        (PurePosixPath("/f1/f3/"), "f3"),
        (PurePosixPath("/f1/f3"), "f3"),
        (PurePosixPath("/f1/f3/index"), "f3"),
        (PurePosixPath("/f1/f3/"), "f3"),
        (PurePosixPath("/f1/f3/d3"), "d3"),
        (PurePosixPath("/f1/f3/d3/"), "d3"),
    ],
)
def test_find_resource(path: PurePosixPath, expected: str, site: Site) -> None:
    """Use the site fixture to see if find_resource logic works."""
    resource = find_resource(site, path)
    assert resource.name == expected


def test_find_resource_missing_slash(site: Site) -> None:
    """Missing slash at path beginning should give ValueError."""
    path = PurePosixPath("f1/XXX")
    with pytest.raises(ValueError) as exc:
        find_resource(site, path)
    expected = 'ResourceLike path "f1/XXX" must start with a slash'
    assert expected == exc.value.args[0]


@pytest.mark.parametrize(
    "path, expected",
    [
        (PurePosixPath("/XXX"), 'No resource at path "/XXX"'),
        (PurePosixPath("/f1/XXX"), 'No resource at path "/f1/XXX"'),
    ],
)
def test_find_resource_failed(path: PurePosixPath, expected: str, site: Site) -> None:
    """Provide a bogus path and get a LookupError."""
    with pytest.raises(KeyError) as exc:
        find_resource(site, path)
    assert expected == exc.value.args[0]


@pytest.mark.parametrize(
    "this_path, expected",
    (
        (PurePosixPath("/"), ()),
        (PurePosixPath("/f1/"), ((None, PurePosixPath("/")),)),
        (PurePosixPath("/d1"), ((None, PurePosixPath("/")),)),
        (
            PurePosixPath("/f1/d2"),
            (
                (None, PurePosixPath("/")),
                ("f1", PurePosixPath("/f1/")),
            ),
        ),
        (
            PurePosixPath("/f1/f3/"),
            (
                (None, PurePosixPath("/")),
                ("f1", PurePosixPath("/f1/")),
            ),
        ),
        (
            PurePosixPath("/f1/f3/d3"),
            (
                (None, PurePosixPath("/")),
                ("f1", PurePosixPath("/f1/")),
                ("f3", PurePosixPath("/f1/f3/")),
            ),
        ),
    ),
)
def test_parents(
    this_path: PurePosixPath,
    expected: tuple[tuple[str, PurePosixPath]],
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
        (PurePosixPath("/"), PurePosixPath("/")),
        (PurePosixPath("/f1"), PurePosixPath("/f1/")),
        (PurePosixPath("/f1/"), PurePosixPath("/f1/")),
        (PurePosixPath("/d1"), PurePosixPath("/d1/")),
        (PurePosixPath("/d1/"), PurePosixPath("/d1/")),
        (PurePosixPath("/f1/d2"), PurePosixPath("/f1/d2/")),
        (PurePosixPath("/f1/d2/"), PurePosixPath("/f1/d2/")),
        (PurePosixPath("/f1/f3"), PurePosixPath("/f1/f3/")),
        (PurePosixPath("/f1/f3/"), PurePosixPath("/f1/f3/")),
        (PurePosixPath("/f1/f3/d3"), PurePosixPath("/f1/f3/d3/")),
        (PurePosixPath("/f1/f3/d3/"), PurePosixPath("/f1/f3/d3/")),
    ),
)
def test_resource_path(
    target: PurePosixPath, expected: PurePosixPath, site: Site
) -> None:
    """Check nested resource paths."""
    r = find_resource(site, target)
    path = resource_path(r)
    assert expected == path


@pytest.mark.parametrize(
    "current, target, expected",
    [
        (PurePosixPath("/index"), PurePosixPath("/index"), PurePosixPath("index")),
        (PurePosixPath("/d1"), PurePosixPath("/d1"), PurePosixPath("d1")),
        (PurePosixPath("/d1/"), PurePosixPath("/d1"), PurePosixPath("d1")),
        (
            PurePosixPath("/f1/f3/index"),
            PurePosixPath("/f1/d2"),
            PurePosixPath("../d2"),
        ),
        (PurePosixPath("/f1/f3/d3"), PurePosixPath("/d1"), PurePosixPath("../../d1")),
        (
            PurePosixPath("/f1/f3/d3"),
            PurePosixPath("/index"),
            PurePosixPath("../../index"),
        ),
        (
            PurePosixPath("/f1/f3/d3"),
            PurePosixPath("/f1/index"),
            PurePosixPath("../index"),
        ),
        (
            PurePosixPath("/f1/f3/d3"),
            PurePosixPath("/f1/f3/index"),
            PurePosixPath("index"),
        ),
        (PurePosixPath("/d1"), PurePosixPath("/f1/f3/d3/"), PurePosixPath("f1/f3/d3")),
        (
            PurePosixPath("/f1/f3/index"),
            PurePosixPath("/index"),
            PurePosixPath("../../index"),
        ),
        (
            PurePosixPath("/f1/f3/index"),
            PurePosixPath("/f1/index"),
            PurePosixPath("../index"),
        ),
        (
            PurePosixPath("/f1/f3/index"),
            PurePosixPath("/f1/f3/d3"),
            PurePosixPath("d3"),
        ),
        (PurePosixPath("/index"), PurePosixPath("/d1"), PurePosixPath("d1")),
        (PurePosixPath("/d1"), PurePosixPath("/index"), PurePosixPath("index")),
    ],
)
def test_relative_path(
    current: PurePosixPath,
    target: PurePosixPath,
    expected: PurePosixPath,
) -> None:
    """Check relative paths between a source and a target."""
    result = relative_path(current, target)
    assert expected == result


@pytest.mark.parametrize(
    "current, expected",
    [
        (PurePosixPath("/index"), PurePosixPath("static/css/styles.css")),
        (PurePosixPath("/d1"), PurePosixPath("static/css/styles.css")),
        (PurePosixPath("/f1/index"), PurePosixPath("../static/css/styles.css")),
        (PurePosixPath("/f1/f3/index"), PurePosixPath("../../static/css/styles.css")),
        (PurePosixPath("/f1/f3/d3"), PurePosixPath("../../static/css/styles.css")),
    ],
)
def test_relative_path_static(current: PurePosixPath, expected: PurePosixPath) -> None:
    """Relative paths between two resources, but involving the static path."""
    root_path = PurePosixPath("/")
    target = PurePosixPath("css/styles.css")
    static_prefix = PurePosixPath("static")

    rp = relative_path(current, root_path, static_prefix=static_prefix)
    result = rp / target
    assert expected == result


@pytest.mark.parametrize(
    "current, expected",
    (
        (PurePosixPath("/"), PurePosixPath("/index")),
        (PurePosixPath("/index"), PurePosixPath("/index")),
        ("site", PurePosixPath("/index")),
        ("site", PurePosixPath("/index")),
        ("/f1/d2", PurePosixPath("/f1/d2")),
    ),
)
def test_normalize(
    current: PurePosixPath | str, expected: PurePosixPath, site: Site
) -> None:
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
        (PurePosixPath("/"), PurePosixPath("/"), None, None, PurePosixPath("index")),
        (
            PurePosixPath("/"),
            PurePosixPath("/"),
            None,
            ".html",
            PurePosixPath("index.html"),
        ),
        (
            PurePosixPath("/index"),
            PurePosixPath("/"),
            None,
            None,
            PurePosixPath("index"),
        ),
        (
            PurePosixPath("/"),
            PurePosixPath("/index"),
            None,
            None,
            PurePosixPath("index"),
        ),
        (
            PurePosixPath("/f1/d2"),
            PurePosixPath("/d1"),
            None,
            None,
            PurePosixPath("d1"),
        ),
        (
            PurePosixPath("/f1/d2"),
            PurePosixPath("/d1"),
            None,
            ".html",
            PurePosixPath("d1.html"),
        ),
        (
            PurePosixPath("/f1/d2"),
            PurePosixPath("icon.png"),
            PurePosixPath("/xxx"),
            None,
            PurePosixPath("/xxx/icon.png"),
        ),
    ),
)
def test_relative(
    current: PurePosixPath,
    target: PurePosixPath,
    static_prefix: PurePosixPath | None,
    suffix: str | None,
    expected: PurePosixPath,
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
    target = PurePosixPath("/foo/bar/baz")
    result = srp(target)
    assert PurePosixPath("../foo/bar/baz.html") == result


@pytest.fixture
def nullster_path() -> Path:
    """Get the filesystem location of the nullster package."""
    from themester import nullster

    return Path(nullster.__file__)


def test_factory_static_relative_path(site: Site, nullster_path: Path) -> None:
    """Get the relative path to a static asset."""
    this_static_src = StaticSrc(
        here=nullster_path,
        source=nullster_path.parent / "static/nullster.css",
    )
    resource = site["d1"]
    srp = StaticRelativePath(
        resource=cast(Resource, resource),
        static_src=this_static_src,
    )
    target = PurePosixPath("images/favicon.ico")
    result = srp(target)
    assert PurePosixPath("static/images/favicon.ico") == result


def test_here_one_level() -> None:
    """Resolve a path one level deep."""
    this_source = Path(".")  # nullster/tests/factories
    here = StaticSrc(here=Path(__file__), source=this_source)
    expected = Path(__file__).parent
    assert expected == here.source
    target = Path("../tests/test_url.py")
    result = here(target)
    assert Path("test_url.py") == result


def test_here_two_levels() -> None:
    """Resolve a path two levels deep."""
    this_source = Path("..")  # themabaster/tests
    here = StaticSrc(here=Path(__file__), source=this_source)
    expected = Path(__file__).parent.parent
    assert expected == here.source
    target = Path("../tests/test_url.py")
    result = here(target)
    assert Path("tests/test_url.py") == result


def test_here_three_levels() -> None:
    """Resolve a path three levels deep."""
    this_source = Path("../..")  # themabaster
    here = StaticSrc(here=Path(__file__), source=this_source)
    expected = Path(__file__).parent.parent.parent
    assert expected == here.source

    target = Path("../../tests/test_url.py")
    result = here(target)
    assert Path("tests/test_url.py") == result
