"""Sample views for a Nullster theme."""
from dataclasses import dataclass

from hopscotch.operators import get
from viewdom import VDOM
from viewdom import html

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
        # language=HTML
        return html(f"""
<html lang="en">
  <head>
    <title>{self.resource_title} - {self.page_title}</title>
  </head>
  <body>
  <main>{self.resource_title} - {self.page_title}</main>  
  </body> 
</html>
        """)
