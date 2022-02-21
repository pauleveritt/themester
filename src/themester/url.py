import inspect
from collections.abc import Mapping
from dataclasses import dataclass
from dataclasses import field
from itertools import repeat
from pathlib import Path
from pathlib import PurePath
from typing import cast
from typing import Iterable
from typing import List
from typing import Optional

from hopscotch import injectable

from themester.protocols import Resource
from themester.resources import Site

ROOT = PurePath("/")
ROOT_PATHS = ("/", "/index", PurePath("/"), PurePath("/index"))


def find_resource(root: Site, path: PurePath) -> Resource:
    """Given a path-like string, walk the tree and return object.

    Resources in a resource tree can be found with path-like lookups.
    This implementation uses ``PurePath`` as the path language.

    Paths must start with a leading ``/``, but a trailing slash is optional.
    Folder paths can be with or without a trailing ``index`` part.
    If the provided path ends with ``index``, it will be removed for the purposes of walking the resource tree.

    Args:
        root: The top of the resource tree.
        path: A specification of how to walk down to the target resource.

    Returns:
        The resource at that path.

    Raises:
        ValueError: Paths must start with a slash.
        KeyError: Asking for a path part that isn't in the dict at that
            part of the tree.
    """

    if not path.is_absolute():
        # ResourceLike paths must start with a slash, so this is
        # probably a static resource path
        m = f'ResourceLike path "{path}" must start with a slash'
        raise ValueError(m)

    # "Normalize" the path if it ends with ``index``.
    pp = path.parts
    # noinspection PyTypeChecker
    parts = iter(pp[1:-1] if path.name == "index" else pp[1:])

    # Now walk the tree
    # TODO: Fix the algorithm here to not need all the cast()
    result = root
    while True:
        try:
            part = next(parts)
            try:
                result = result[part]  # type: ignore
            except KeyError:
                m = f'No resource at path "{path}"'
                raise KeyError(m)
        except StopIteration:
            break
    return cast(Resource, result)


def parents(resource: Resource) -> Iterable[Resource]:
    """Parents of a resource, reversed: parent, then grandparent, etc.

    Args:
        resource: The target resource to get the parents of.

    Returns:
        A tuple of zero (root is target) or more resources.
    """

    these_parents: List[Resource] = []
    parent = resource.parent
    while parent is not None:
        these_parents.append(parent)
        parent = parent.parent

    return reversed(these_parents)


def relative_path(
    current: PurePath,
    target: PurePath,
    static_prefix: Optional[PurePath] = None,
) -> PurePath:
    """
    Calculate a dotted path from a source to destination.

    Relative paths are hard.
    Lots of edge cases, lots of configurable policies.
    This function is the innermost logic, which presumes lots of complexity is handled before stuff gets passed in.

    Themester's logic is based on Python's ``PurePath``: a virtual hierarchy that is sort of like the filesystem, but not actually tied to a filesystem.
    References to documents in the site and static assets are done as these virtual pure paths.
    Static asset references are "normalized" at definition time to be relative to a configurable site root.

    Both ``current`` and ``target`` are expected to start with a slash.
    It doesn't matter if it does or doesn't end with a slash.

    This function doesn't care about whether folders should get ``/index`` added to their path.
    In fact, it doesn't understand folders.
    It expects to the path to include ``index`` when current or target are a collection of some kind.

    Policies handled before this is called:

    - Adding '/index' to current/target if it is a collection

    - Adding a configurable suffix such as ``index.html``

    - Converting a resource to a path

    - Detecting a resource is a collection and should get ``index`` added to path

    Args:
        current: Source from which target is relative, with leading slash
        target: Destination, with leading slash
        static_prefix: Path to insert between dots and target
    """

    if not current.is_absolute():
        m = f'Source path "{str(current)}" must start with a slash'
        raise ValueError(m)

    if static_prefix is None and not target.is_absolute():
        m = f'Target path "{str(target)}" must start with a slash'
        raise ValueError(m)

    # Do an optimization...bail out immediately if the same, but make
    # it relative
    if current == target:
        return PurePath(current.name)

    # noinspection PyTypeChecker
    current_parents = iter(current.parents)
    target_parents = target.parents

    result: Optional[PurePath] = None
    hops = -1

    while True:
        try:
            result = next(current_parents)
            hops += 1
            if result in target_parents:
                raise StopIteration()
        except StopIteration:
            break

    # What is the "leftover" part of target
    remainder_parts = target.relative_to(str(result))

    # How many hops up to go
    prefix = PurePath("/".join(repeat("..", hops)))

    # Join it all together
    if static_prefix is None:
        v = prefix.joinpath(remainder_parts)
    else:
        v = prefix.joinpath(static_prefix, remainder_parts)
    return v


def resource_path(resource: Resource) -> PurePath:
    """Return a path representation of resource.

    The resource should be location-aware, meaning, it has a ``name`` and a ``parent`` attributes.

    - Always with a leading slash
    - Never with a trailing slash
    - No ``index`` at the end of a collection

    Args:
        resource: The target to get the path for.

    Returns:
        A PurePath with representation.
    """

    # Bail out quickly if we are the root or in the root
    root_path = PurePath("/")

    if resource.parent is None:
        return root_path
    elif resource.parent.parent is None and resource.name is not None:
        return root_path / resource.name

    lineage = list(parents(resource))
    lineage.append(resource)

    # Get the names for each part, then join with slashes
    parts = [
        PurePath(p.name) if p.name is not None else PurePath("/") for p in lineage if p
    ]
    path = root_path.joinpath(*parts)
    return path


def normalize(item: Resource | PurePath | str) -> PurePath:
    """
    Convert current or target to a PurePath.

    The relative function below liberally accepts a PurePath, ResourceLike, or str for current/target.
    Convert to PurePath.

    Args:
         item: The object to make into a "normalized" PurePath.
    """

    # Quick convenience check, root always results in PurePath('/index')
    if item in ROOT_PATHS:
        return PurePath("/index")

    if isinstance(item, PurePath):
        normalized_item = item
    elif hasattr(item, "parent"):
        # Crappy way to check if something is a ResourceLike
        normalized_item = resource_path(cast(Resource, item))
        if isinstance(item, Mapping):
            # Add /index
            normalized_item = normalized_item / "index"
    else:
        # Presume it is a string conforming to the path rules, though it
        # might be a non-resource object (no parent)
        assert isinstance(item, str)  # This shouldn't fail
        normalized_item = PurePath(item)

    return normalized_item


def relative(
    current: Resource | PurePath | str,
    target: Resource | PurePath | str,
    static_prefix: Optional[PurePath] = None,
    suffix: Optional[str] = None,
) -> PurePath:
    """
    Get a path but with all the framework policies on the way in/out.

    As mentioned in ``relative_path``, there are parts of the logic that it doesn't handle.
    It expects everything to be "normalized": PurePaths on both sides, no concept of ``index`` for folders, no configurable ``.html`` suffix.
    This function does those things.

    Args:
        current: The resource, path, or string for source.
        target: The resoure, path, or string for destination.
        static_prefix: If resolving a static asset, provide this.
        suffix: If resolving a resource, provide file extension.
    """

    # Normalize to a PurePath
    normalized_current = normalize(current)
    normalized_target = normalize(target)

    # Are we resolving a static resource?
    if static_prefix is None:
        value = relative_path(
            normalized_current,
            normalized_target,
        )
        if suffix is not None:
            value = value.with_suffix(suffix)
    else:
        value = relative_path(
            normalized_current,
            ROOT,
            static_prefix=static_prefix,
        )
        value = value / normalized_target
    return value


@dataclass
class StaticSrc:
    """Resolve Path objects relative to a static prefix.

    Working with static paths is hard. ``pathlib.Path.resolve()`` and
    friends work on the basis of ``os.get_cwd()`` instead of the
    location where something is defined.

    Allow creating an instance to record the ``static_source`` that
    acts as a prefix for all future resolving. Then, the ``__call__``:

    - Use stacks to find the module where it is called
    - Accept an argument for a relative ``Path`` to a static asset
    - Turn that into a full/absolute/resolved path
    - Trim off the static_prefix
    - Return a ``PurePath`` that is relative to the ``static_source`` dir
    """

    here: Path
    source: Path

    def __post_init__(self) -> None:
        parent = Path(self.here).parent
        target_path = parent.joinpath(self.source)
        self.source = target_path.resolve()

    def __call__(self, target: Path) -> PurePath | None:
        """Make the target relative to the site's static directory"""

        # Get a Path() pointed at the caller's directory
        frame = inspect.stack()[1]
        module = inspect.getmodule(frame[0])
        if module and module.__file__:
            module_path = Path(module.__file__).parent
            target_path = module_path.joinpath(target).resolve()

            # Chop off the part of the path in the beginning that overlaps
            # with the site's static_source
            value = target_path.relative_to(self.source)
            return value

        else:
            # Should only get here if frame[0] isn't a module
            raise ValueError("No module")


@injectable()
@dataclass
class StaticDest:
    """
    Configure the relative path to the static output dir.

    Our rendering needs to generate links to the static dir. This
    might be different for different systems. For example, Sphinx
    uses `_static` (and in fact, makes it configurable.)
    """

    dest: PurePath = PurePath("static")


@injectable()
@dataclass
class RelativePath:
    """
    Convert path to resource to a relative path.
    """

    resource: Resource
    suffix: str = ".html"  # TODO Get this from config

    def __call__(
        self,
        target: Resource | PurePath | str,
    ) -> PurePath:
        """
        Convert a resource path to a relative path with a suffix.

        Args:
             target: Full path to resource starting from root.
        """

        value = relative(
            current=self.resource,
            target=target,
            suffix=self.suffix,
        )

        return value


@injectable()
@dataclass
class StaticRelativePath:
    """
    Convert path to static asset to a relative path.
    """

    resource: Resource
    static_src: StaticSrc
    static_dest: StaticDest = field(default_factory=StaticDest)

    def __call__(
        self,
        target: Resource | PurePath | str,
    ) -> PurePath:
        """Convert an asset path to a relative path.

        The configs etc. will point at a static asset in the theme file.
        It needs to be converted to a relative path, to the static directory.

        The target path is "normalized" to be relative to the static *source*.
        Meaning, if the theme has ``some_static/images/favicon.ico``, it is
        expected that the value passed here is
        ``PurePath('images/favicon.ico')``. This is usually done through the
        use of the ``StaticHere`` constructor as assignment time.

        Args:
             target: Path relative to ``StaticConfig.source``.
        """

        value = relative(
            current=self.resource,
            target=target,
            static_prefix=self.static_dest.dest,
        )

        return value
