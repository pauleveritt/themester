"""Sample views for a Nullster theme."""
from dataclasses import dataclass

from hopscotch.operators import get
from viewdom import html
from viewdom import VDOM

from themester.decorators import view
from themester.protocols import Resource
from themester.url import StaticRelativePath


@view()
@dataclass
class IndexView:
    """Default view for all contexts."""

    srp: StaticRelativePath
    resource_title: str = get(Resource, attr="title")
    page_title: str = "View"

    def __call__(self) -> VDOM:
        """Render the view."""
        nullster_css = self.srp("nullster.css")
        return html(
            f"""
<html lang="en">
  <head>
    <title>{self.resource_title} - {self.page_title}</title>
    <link rel="stylesheet" href={nullster_css!s}/>
  </head>
  <body>
  <main>{self.resource_title} - {self.page_title}</main>
  </body>
</html>
        """
        )
