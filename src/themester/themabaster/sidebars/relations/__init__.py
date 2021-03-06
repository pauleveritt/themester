"""
Sidebar to show related topics previous/next/parents.
"""

from dataclasses import dataclass, field
from typing import Callable, Optional

from markupsafe import Markup
from viewdom import VDOM, html
from viewdom_wired import component
from wired.dataclasses import injected
from wired_injector.operators import Get

from themester.sphinx.config import SphinxConfig
from themester.sphinx.models import PageContext

try:
    from typing import Annotated
except ImportError:
    from typing_extensions import Annotated


@component()
@dataclass
class Relations:
    master_doc: Annotated[str, Get(SphinxConfig, attr='master_doc')]
    pathto: Annotated[Callable[[str], str], Get(PageContext, attr='pathto')]
    toctree: Annotated[Optional[Callable[[], str]], Get(PageContext, attr='toctree')]
    resolved_pathto: str = field(init=False)
    resolved_toctree: Markup = field(init=False)

    def __post_init__(self):
        self.resolved_pathto = self.pathto(self.master_doc)
        self.resolved_toctree = Markup(self.toctree())

    def __call__(self) -> VDOM:
        # Alabaster has a weird relations.html which isn't really well-formed
        # on looping. This makes it not-well-formed on snippets.
        return html('''\n
<div class="relations">
    <h3>Contents</h3>
    <ul>
        <li><a href={self.resolved_pathto}>Documentation overview</a>
        </li>
    </ul>
    {self.resolved_toctree}
</div>
        ''')
