Themester extensions have a second pass at configuration, after Sphinx
itself has been config'd and extension setup() functions
have been called.

If an extension has a `svcs_setup` function, it will be
called with the registry, which has all the Sphinx config
and setup available as factories.
