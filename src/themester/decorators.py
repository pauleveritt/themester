"""Convenience decorators for custom Themester injectables."""

from hopscotch import injectable

from themester.protocols import View, Config


# noinspection PyPep8Naming
class view(injectable):
    kind = View


# noinspection PyPep8Naming
class config(injectable):
    kind = Config
