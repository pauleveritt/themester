from dataclasses import dataclass, field
from typing import Tuple

from viewdom import html, VDOM
from viewdom_wired import component
from wired_injector.operators import Get

from themester.operators import StaticPathTo, Paths
from themester.protocols import ThemeConfig
from themester.sphinx import HTMLConfig
from themester.sphinx.models import PageContext

try:
    from typing import Annotated
except ImportError:
    from typing_extensions import Annotated


def JSFile(src: str) -> VDOM:
    """ Small anonymous component used with the parent """
    return html('<script type="text/javascript" src={src}>//</script>')


@component()
@dataclass
class JSFiles:
    site_files: Annotated[
        Paths,
        Get(HTMLConfig, attr='js_files'),
        StaticPathTo(),
    ]
    theme_files: Annotated[
        Paths,
        Get(ThemeConfig, 'js_files'),
        StaticPathTo(),
    ]
    page_files: Annotated[
        Paths,
        Get(PageContext, 'js_files'),
        StaticPathTo(),
    ]
    srcs: Tuple[str, ...] = field(init=False)

    def __post_init__(self):
        self.srcs = self.site_files + self.theme_files + self.page_files

    def __call__(self) -> VDOM:
        return html('{[JSFile(src) for src in self.srcs]}')
