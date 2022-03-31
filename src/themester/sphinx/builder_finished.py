"""Event handlers for the Sphinx ``builder-finished`` event."""

import shutil
from pathlib import Path

from hopscotch import Registry
from sphinx.application import Sphinx

from themester.url import StaticSrc


def copy_theme_resources(static_src: Path, output_dir: Path) -> None:
    """Get the theme's resources and copy to Sphinx output directory."""
    static_resources = static_src.glob('**/*')
    for static_resource in static_resources:
        if static_resource.is_dir():
            shutil.copytree(static_resource, output_dir / static_resource.name, dirs_exist_ok=True)
        else:
            shutil.copyfile(static_resource, output_dir / static_resource.name)


def setup(
    app: Sphinx,
    exc: Exception,
) -> None:
    """Wire up an event handler for builder-finished."""
    if exc is None:
        registry: Registry = getattr(app, "site_registry")
        try:
            static_src = registry.get(StaticSrc).source
            output_dir = Path(app.outdir) / '_static'
            copy_theme_resources(static_src, output_dir)
        except LookupError:
            # No StaticSrc so the theme doesn't want to do this
            raise ValueError(2323)
