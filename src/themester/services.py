"""Various Sphinx utilities as factories in svcs."""

from dataclasses import dataclass
from typing import Any, cast
from urllib.parse import quote

from sphinx.builders import Builder
from sphinx.builders.html import StandaloneHTMLBuilder

from svcs import Container

SEP = "/"


@dataclass(frozen=True)
class RelativeUri:
    """Return a relative URL from ``base`` to ``to``."""

    container: Container

    def __call__(self, base: str, to: str) -> str:
        if to.startswith(SEP):
            return to
        b2 = base.split("#")[0].split(SEP)
        t2 = to.split("#")[0].split(SEP)
        # remove common segments (except the last segment)
        for x, y in zip(b2[:-1], t2[:-1], strict=False):
            if x != y:
                break
            b2.pop(0)
            t2.pop(0)
        if b2 == t2:
            # Special case: relative_uri('f/index.html','f/index.html')
            # returns '', not 'index.html'
            return ""
        if len(b2) == 1 and t2 == [""]:
            # Special case: relative_uri('f/index.html','f/') should
            # return './', not ''
            return "." + SEP
        return (".." + SEP) * (len(b2) - 1) + SEP.join(t2)


@dataclass(frozen=True)
class BuilderConfig:
    """Wrapper around getting config options from the builder."""

    container: Container

    def __call__(self, option: str, default: str) -> Any:
        """Return a builder specific option.

        This method allows customization of common builder settings by
        inserting the name of the current builder in the option key.
        If the key does not exist, use default as builder name.
        """
        # At the moment, only XXX_use_index is looked up this way.
        # Every new builder variant must be registered in Config.config_values.
        builder = self.container.get(Builder)
        try:
            optname = f"{builder.name}_{option}"
            return getattr(builder.config, optname)
        except AttributeError:
            optname = f"{default}_{option}"
            return getattr(builder.config, optname)


@dataclass(frozen=True)
class TargetUri:
    """Use quote and link suffix to normalize a docname."""

    container: Container

    def __call__(self, docname: str, typ: str | None = None) -> str:
        builder_config = self.container.get(BuilderConfig)
        html_link_suffix = builder_config("link_suffix", "html")

        html_file_suffix = builder_config("file_suffix", "html")
        if html_file_suffix is not None:
            # TODO Adam This path means out_suffix might never get set
            #   This is from builders/__init__.py line 182
            out_suffix = html_file_suffix

        if html_link_suffix is not None:
            link_suffix = html_link_suffix
        else:
            link_suffix = out_suffix

        return quote(docname) + link_suffix


@dataclass(frozen=True)
class PathTo:
    container: Container

    def __call__(
        self,
        pagename: str,
        otheruri: str,
        resource: bool = False,
        baseuri: str | None = None,
    ):
        target_uri = self.container.get(TargetUri)
        relative_uri = self.container.get(RelativeUri)
        if baseuri is None:
            # in the singlehtml builder, default_baseuri still contains an #anchor
            # part, which relative_uri doesn't really like...
            # If no baseuri passed in, use "defaultbaseuri"
            baseuri = target_uri(pagename).rsplit("#", 1)[0]
        if resource and "://" in otheruri:
            # allow non-local resources given by scheme
            return otheruri
        elif not resource:
            otheruri = target_uri(otheruri)
        uri = relative_uri(baseuri, otheruri) or "#"
        builder = cast(StandaloneHTMLBuilder, self.container.get(Builder))
        if uri == "#" and not builder.allow_sharp_as_current_path:
            uri = baseuri
        return uri
