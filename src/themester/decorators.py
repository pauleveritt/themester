"""Convenience decorators for custom Themester injectables."""
from hopscotch import injectable

from themester.protocols import Config
from themester.protocols import View


# noinspection PyPep8Naming
class view(injectable):  # noqa: N801
    """Injectable views."""

    kind = View


# noinspection PyPep8Naming
class config(injectable):  # noqa: N801
    """Injectable configuration information."""

    kind = Config
