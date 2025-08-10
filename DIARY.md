# Diary

Running log of notes to later turn into docs.

## Aug 10 2025



## Aug 9 2025

Adam Turner messaged me, interested in the registry and view ideas. Let's bring `themester-sphinx` back in and get
everything working again.

I put everything in `themester.sphinx` for now. The first focus: just getting everything from the `themester-sphinx`
package copied over. Let's go back to making Themester a Sphinx-first for now.

The big effort: extracting `PathTo` into a service. The real Sphinx implementation, not my previous Themester nor Goku
services that were not tied to Sphinx. It was important to have a backwards-compatible starting point.

I'm still going to need the neutral ones. But I will do this *after* I branch off from a PoC for Adam.

## May 31

`themester-sphinx` needs to implement a protocol that will be in Themester. That
would make `themester-sphinx` depend on `Themester`. Which is ok, but I don't
want to set up my workspaces like that just yet. Instead: protocols! It's the
shape, not the name...hopefully.

## May 25

After some research in Sphinx collectors and environments, I chickened out: I
will do the minimum to keep moving. I will also hold off on moving everything to
`Path`. Otherwise, I kept the Themester strategy of "normalizing" the big pile
of the page `context` dict into a dataclass. Ultimately I could just provide a
`TypedDict` instead of transforming the original data. However, that's kind of
the goal for this project: craft a new, modern API.

Looks like builder-finished isn't needed in this package. It's focused on
themes, copying static resources, belongs in Themester.

As it turns out, this package will be quite small for now.

Ok, I did it: I changed this to `themester-sphinx`. I'll wait until later to
tackle "refactor all of Sphinx around svcs and hexagonal."

## May 24

Tackling HTML page context. This is fun, lots of complexity that could be
isolated by svcs.

To start, I'm reminded of some of the decisions to make. Such as escaping the
body. Sphinx already depends on `Markupsafe`. But `tdom` wanted to go in a
direction to not depend on it. However, this package isn't intended to scratch
the itch of Themester and tdom. It's for reinventing Sphinx development (and
helping Themester along the way.) Thus: let's use Markupsafe.

As I pick apart Themester's `make_page_context`, I see some of the shortcuts
taken. I didn't expose all the granularity that I could. The ToC and document
metadata that are part of the `context` object passed into the
`html-page-context` event should be services. Hopefully, svcs can handle
dependency ordering. Let's see.

## May 21

Screw it, I'm adding a `package.json` to get Prettier on Markdown. Don't hate
me. I'll make a `.gitignore` and keep that out of the repo.

Themester and Goku had a system where you could put a function in your
`conf.py`. If present, `builder-init` would call it with the registry, and you
could add stuff conveniently, just for your project. Let's bring that over, with
tests. This probably will be a common pattern for all Themester-supported
targets. We will make the function `svcs_setup`. It will be invoked last, after
Sphinx stuff is added to the registry. I'll start by adding something to
`test-sphinx-svcs-setup` that fails.

I wanted to make `venusian` optional. But it's complicated. My fastest path to
the end of all these packages is to make it mandatory and get the `Scanner` into
the registry. The scanner will have the `site_registry`.

## May 20

Get started with a `uv init` targeting 3.10 or higher.

Get Sphinx test roots setup with pytest and conftest.py. I took a look at what's
in Sphinx for the fixtures, but also copied over some of my previous work. I
started with my BeautifulSoup fixtures, but I'm not really going to be testing
HTML output, so simplify the dependencies.

Start some Sphinx setup functions to wire in builder-inited and get tests that
find the registry in the SphinxTestApp.

We name the svcs registry as app.site_registry to avoid conflicting with
Sphinx's app.registry.
