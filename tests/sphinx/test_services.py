from dataclasses import dataclass

import pytest
from sphinx.builders import Builder

from themester.sphinx.models import PageContext
from themester.sphinx.services import BuilderConfig, TargetUri, RelativeUri, PathTo


@pytest.fixture
def builder():
    @dataclass
    class FakeBuilderConfig:
        html_file_suffix: str = ".html"
        html_link_suffix: str = ".html"
        xxx_some_option: str = "xxx value"

    @dataclass
    class FakeBuilder:
        name: str
        config: FakeBuilderConfig

    config = FakeBuilderConfig()
    return FakeBuilder(name="html", config=config)


@pytest.fixture
def builder_config(builder):
    container = {
        Builder: builder,
    }
    return BuilderConfig(container=container)


def test_builder_config_default(builder):
    """Test the wrapper around the Sphinx builder config fetcher."""

    container = {
        Builder: builder,
    }
    builder_config = BuilderConfig(container=container)
    result = builder_config("link_suffix", "html")
    assert result == ".html"


def test_builder_config_different_default(builder_config):
    """Test the wrapper around the Sphinx builder config fetcher."""

    # This should not use the "default" arg
    result1 = builder_config("link_suffix", "xxx")
    assert result1 == ".html"
    # # This should also not use the "default" arg
    result2 = builder_config("link_suffix", "html")
    assert result2 == ".html"
    # This SHOULD use the "default" arg
    result3 = builder_config("some_option", "xxx")
    assert result3 == "xxx value"


def test_target_uri(builder_config):
    """Convert a docname into a suitable target."""

    container = {
        BuilderConfig: builder_config,
    }
    target_uri = TargetUri(container=container)
    result = target_uri("somedocname")
    assert result == "somedocname.html"


def test_relative_uri():
    """Convert a docname into a suitable target."""
    container = {}
    relative_uri = RelativeUri(container=container)
    result = relative_uri(base="/root/f1/current", to="../f2/target")
    assert result == "../../../../f2/target"


def test_pathto(builder, builder_config):
    """Check all of Sphinx's policies for path handling."""

    @dataclass
    class FakePageContext:
        pagename: str = "fakepage.html"

    container = {
        TargetUri: TargetUri(
            container={
                BuilderConfig: builder_config,
            }
        ),
        RelativeUri: RelativeUri(container={"Builder": builder}),
        Builder: builder,
        PageContext: FakePageContext(),
    }
    path_to = PathTo(container=container)
    result = path_to(otheruri="someotheruri")
    assert result == "someotheruri.html"
