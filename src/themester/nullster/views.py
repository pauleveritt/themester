"""Sample views for a Nullster theme."""
from dataclasses import dataclass

from hopscotch.operators import get
from viewdom import html
from viewdom import VDOM

from themester.decorators import view
from themester.protocols import Resource


@view()
@dataclass
class IndexView:
    """Default view for all contexts."""

    resource_title: str = get(Resource, attr="title")
    page_title: str = "View"

    def __call__(self) -> VDOM:
        """Render the view."""
        return html(f"<title>{self.resource_title} - {self.page_title}</title>")
