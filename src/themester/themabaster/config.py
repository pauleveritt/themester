"""

An implementation of the protocol for all the knobs for this layout.

In Sphinx, this would be an instance that was left in the ``conf.py``
file then injected into the site container as a singleton.
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, Tuple, Callable, Sequence

from themester.protocols import ThemeConfig
from themester.sphinx.models import Links


@dataclass
class FaviconSize:
    size: str
    filename: str


@dataclass
class Favicons:
    """ Configure a potential set of ico/png images at different sizes.

    Presumes images are in the static directory once deployed and are relative to it.
     """

    shortcut: Optional[str] = 'favicon.ico'
    png: Optional[str] = 'apple-touch-icon-precomposed.png'
    sizes: Optional[Sequence[FaviconSize]] = (
        FaviconSize(size='72x72', filename='apple-touch-icon-144x144-precomposed.png'),
        FaviconSize(size='114x114', filename='apple-touch-icon-114x114-precomposed.png'),
        FaviconSize(size='144x144', filename='apple-touch-icon-72x72-precomposed.png'),
    )


def get_sidebars():
    """ Escape circular import hell """

    from .sidebars.localtoc import LocalToc
    from .sidebars.relations import Relations
    from .sidebars.searchbox import SearchBox
    from .sidebars.sourcelink import SourceLink
    return (
        LocalToc,
        Relations,
        SourceLink,
        SearchBox,
    )


@dataclass(frozen=True)
class ThemabasterConfig(ThemeConfig):
    # HTML Builder
    sidebars: Tuple[Callable, ...] = field(default_factory=get_sidebars)

    # Alabaster
    badge_branch: str = 'master'
    codecov_button: bool = False
    codecov_path: Optional[str] = None
    description: Optional[str] = None
    donate_url: Optional[str] = None
    extra_nav_links: Links = None
    github_button: bool = True
    github_count: str = 'true'
    github_repo: Optional[str] = None
    github_type: str = 'watch'
    github_user: Optional[str] = None
    opencollective: Optional[str] = None
    opencollective_button_color: str = 'white'
    show_powered_by: bool = True
    show_relbar_bottom: bool = False
    show_relbar_top: bool = False
    show_relbars: bool = False
    sidebar_collapse: bool = True
    sidebar_includehidden = True
    tidelift_url: Optional[str] = None
    travis_button: bool = False
    travis_path: Optional[str] = None

    favicons: Favicons = Favicons()

    # Not in Sphinx/Alabaster
    css_files: Tuple[str, ...] = (
        '_static/themabaster.css',
        '_static/pygments.css',
    )
    js_files: Tuple[str, ...] = tuple()

    @staticmethod
    def get_static_resources() -> Tuple[Path, ...]:
        """ Return all the files that should get copied to the static output """

        static_dir = Path(__file__).parent.absolute() / 'static'
        static_resources = static_dir.glob('**/*')
        return tuple(static_resources)
