"""Test the built-in resources."""
from themester.resources import Site


def test_site(site: Site) -> None:
    """Ensure Site constructs and static types against protocol."""
    assert None is site.name


def test_folder(site: Site) -> None:
    """Ensure Folder constructs and static types against protocol."""
    f = site["f1"]
    assert "f1" == f.name  # type: ignore


def test_document(site: Site) -> None:
    """Ensure Document constructs and static types against protocol."""
    d = site["d1"]
    assert "d1" == d.name  # type: ignore
