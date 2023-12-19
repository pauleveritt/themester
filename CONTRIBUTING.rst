Contributor Guide
=================

Thank you for your interest in improving this project.
This project is open-source under the `MIT license`_ and
welcomes contributions in the form of bug reports, feature requests, and pull requests.

Here is a list of important resources for contributors:

- `Source Code`_
- `Documentation`_
- `Issue Tracker`_
- `Code of Conduct`_

.. _MIT license: https://opensource.org/licenses/MIT
.. _Source Code: https://github.com/pauleveritt/themester
.. _Documentation: https://themester.readthedocs.io/
.. _Issue Tracker: https://github.com/pauleveritt/themester/issues

How to report a bug
-------------------

Report bugs on the `Issue Tracker`_.

When filing an issue, make sure to answer these questions:

- Which operating system and Python version are you using?
- Which version of this project are you using?
- What did you do?
- What did you expect to see?
- What did you see instead?

The best way to get your bug fixed is to provide a test case,
and/or steps to reproduce the issue.


How to request a feature
------------------------

Request features on the `Issue Tracker`_.


How to set up your development environment
------------------------------------------

You need Python 3.7+ and the following tools:

- Hatch_

You can now run an interactive Python session,
or the command-line interface:

.. code:: console

   $ hatch shell

.. _Hatch: https://hatch.pypa.io/latest/

How to test the project
-----------------------

Run the full test suite:

.. code:: console

   $ hatch run test:run


Unit tests are located in the ``tests`` directory,
and are written using the pytest_ testing framework.

.. _pytest: https://pytest.readthedocs.io/

How to set up your PyCharm environment
--------------------------------------

Get test virtualenv interpreter path from hatch:

.. code:: console

   $ hatch env find test.py3.12


You should set up an existing virtualenv interpreter in PyCharm with the path from the previous command.
`follow these instructions`_ for Existing virtual environment

.. _follow these instructions: https://www.jetbrains.com/help/pycharm/creating-virtual-environment.html

How to submit changes
---------------------

Open a `pull request`_ to submit changes to this project.

Your pull request needs to meet the following guidelines for acceptance:

- Include unit tests. This project maintains 100% code coverage.
- If your changes add functionality, update the documentation accordingly.

Feel free to submit early, though—we can always iterate on this.

To run linting and code formatting checks before committing your change, you can install pre-commit as a Git hook by running the following command:

.. code:: console

   $ hatch run pre-commit:install

It is recommended to open an issue before starting work on anything.
This will allow a chance to talk it over with the owners and validate your approach.

.. _pull request: https://github.com/pauleveritt/themester/pulls
.. github-only
.. _Code of Conduct: CODE_OF_CONDUCT.rst
