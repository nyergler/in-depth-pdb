==============
 In Depth PDB
==============

.. note::

   This document was prepared for presentation to the engineering team
   at Eventbrite. It is currently under development; please send
   suggestions to ``nathan+pdb@yergler.net``.

Most developers have a preferred debugging strategy, and many of them
are variations on the ``print`` statement. There's nothing wrong with
that, you can get a lot of information about what a program is doing
by logging information about its state. They fall short, however, in
that you need to know what you want to log before you start: if you
realize after seeing some data that what you really need to know if
the state of some other variable, you usually need to change the print
statements and restart execution.

Debuggers -- and PDB, in particular -- are a more flexible tool for
inspecting the state of a running program. They allow you to
introspect the state of variables, examine the call stack, and in some
cases modify the state of the program without restarting it. This
document introduces PDB, the Python Debugger, and explains how it can
be leveraged effectively.

.. toctree::
   :maxdepth: 1

   getting-started
   invoking
   interacting
   breakpoints
   extending


Other Tools
===========

* ipdb_ is a drop-in replacement for PDB that provides syntax
  highlighting, tab completion, and better introspection.
* rdb_
* pudb_
* ``pdbtrack`` is included with modern distributions of
  `python-mode`_, and allows Emacs to open files as they're debugged
  by PDB. Recent versions add support for `filename mapping`_ which is
  useful when debugging in a SSH session (ie, Eventbrite's
  vagrant-based setup).

Further Reading
===============

* `Tracing Python Code
  <http://www.dalkescientific.com/writings/diary/archive/2005/04/20/tracing_python_code.html>`_
* `Watchpoints in Python <http://sourceforge.net/blog/watchpoints-in-python/>`_

.. _PDB: http://docs.python.org/2/library/pdb.html
.. _`sys.settrace`:  http://docs.python.org/2/library/sys.html#sys.settrace
.. _`command reference`:
.. _`debugger command`:
.. _`debugger commands`: http://docs.python.org/2/library/pdb.html#debugger-commands
.. _`sys.lasttraceback`: http://docs.python.org/2/library/sys.html#sys.last_traceback
.. _ipdb: https://github.com/gotcha/ipdb
.. _rdb: http://dzone.com/snippets/remote-debugging-python-using
.. _`python-mode`: https://launchpad.net/python-mode/
.. _`filename mapping`: http://yergler.net/blog/2012/06/07/mapping-file-paths-for-pdbtrack/
.. _pudb: https://pypi.python.org/pypi/pudb
