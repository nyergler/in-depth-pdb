==============
 In Depth PDB
==============

Getting Started
===============

PDB
---

* Built-in Python debugger
* Inspect the state of running programs
* Repeatedly run a program as you debug it
* Leverages Python's trace function facility
* Extensible tool: ipdb, rdb, etc all build on it

Invoking PDB
============

Explicit Trace Points
---------------------

.. literalinclude:: /samples/fibonacci_trace.py
   :linenos:
   :emphasize-lines: 13

::

   $ python samples/fibonacci_trace.py 5
   > /Users/nathan/p/pdb/samples/fibonacci_trace.py(12)<module>()
   -> print (fib(int(sys.argv[-1])))
   (Pdb)

PDB stops before the first statement in your program is executed,
waiting for a command.


``next``
--------

.. literalinclude:: /samples/fibonacci_trace.py
   :linenos:
   :emphasize-lines: 14

::

   > /Users/nathan/p/pdb/samples/fibonacci_trace.py(14)<module>()
   -> print (fib(sys.argv[-1]))
   (Pdb) n
   ValueError: "invalid literal for int() with base 10: 'samples/fibonacci_trace.py'"
   > /Users/nathan/p/pdb/samples/fibonacci_trace.py(14)<module>()
   -> print (fib(sys.argv[-1]))
   (Pdb)

* ``next`` will execute the next statement (including any calls it
  makes)


``step``
--------

.. literalinclude:: /samples/fibonacci_trace.py
   :linenos:
   :emphasize-lines: 3

::

   > /Users/nathan/p/pdb/samples/fibonacci_trace.py(14)<module>()
   -> print (fib(sys.argv[-1]))
   (Pdb) s
   --Call--
   > /Users/nathan/p/pdb/samples/fibonacci_trace.py(3)fib()
   -> def fib(n):
   (Pdb)

* ``step`` will stop at the next statement (which may be inside a
  function call)


``cont``\ inue
--------------

.. literalinclude:: /samples/fibonacci_trace.py
   :linenos:

::

   > /Users/nathan/p/pdb/samples/fibonacci_trace.py(14)<module>()
   -> print (fib(sys.argv[-1]))
   (Pdb) s
   --Call--
   > /Users/nathan/p/pdb/samples/fibonacci_trace.py(3)fib()
   -> def fib(n):
   (Pdb) cont
   Traceback (most recent call last):
     File "samples/fibonacci_trace.py", line 14, in <module>
       print (fib(sys.argv[-1]))
     File "samples/fibonacci_trace.py", line 3, in fib
       def fib(n):
   ValueError: invalid literal for int() with base 10: 'samples/fibonacci_trace.py'

* ``cont`` will continue execution


Running Under PDB
-----------------

::

   $ python -m pdb samples/fibonacci.py 5
   > /Users/nathan/p/pdb/samples/fibonacci.py(1)<module>()
   -> import sys
   (Pdb)


pdb.run
-------

::

   >>> pdb.run("fib('25')")
   > <string>(1)<module>()
   (Pdb)

::

   >>> pdb.runcall(fib, 25)
   > /Users/nathan/p/pdb/samples/fibonacci.py(7)fib()
   -> if n <= 1:
   (Pdb)

..

   XXX
   The interesting thing to note here is that the next frame for PDB is
   where the error actually occurred, **not** where the debugger was
   called. Try replacing the call to ``post_mortem`` with a call to
   ``set_trace`` to see the difference.


Interacting with Locals
=======================

Inspecting Variables
--------------------


::

  >>> import funcs
  >>> funcs.product_inverses((1,2,3,0))
  Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
    File "funcs.py", line 19, in product_inverses
      result = result * (1.0 / i)
  ZeroDivisionError: float division by zero
  >>> import pdb
  >>> pdb.pm()

::

  > /Users/nathan/p/pdb/samples/funcs.py(19)product_inverses()
  -> result = result * (1.0 / i)
  (Pdb) p result
  0.16666666666666666
  (Pdb) p i
  0
  (Pdb) pp locals()
  {'i': 0, 'ints': (1, 2, 3, 0), 'result': 0.16666666666666666}
  (Pdb)

PDB also has an ``args`` command that will output the arguments passed
to the current function.

::

   (Pdb) args
   ints = (1, 2, 3, 0)

Evaluating Expressions
----------------------

::

   (Pdb) !product_inverses((1, 2, 3))
   0.16666666666666666
   (Pdb)

Note that it's ``product_inverses``, not ``funcs.product_inverses``:
the expression is executed in the context of the code being debugged.

XXX Python 3.2 adds an ``interact`` command.

Modifying Variables
-------------------

XXX

Navigating Execution
====================

Where Am I?
-----------

``where``

``list``

XXX Python 3 list extensions

The Call Stack
--------------

``up``

``down``

Following Execution
-------------------

Review ``step``, ``next``

``return``

``until``

Modifying the Flow
------------------

You can also jump over parts of the code using the cunningly named
``jump`` command.

.. ifnotslides::
   The `command reference`_ points out that "not all jumps are allowed —
   for instance it is not possible to jump into the middle of a for loop
   or out of a finally clause." I don't find many uses for jumps, but
   your mileage may vary.


Breakpoints
===========

Breakpoints vs. set_trace
-------------------------

So far we've talked about how to enter the debugger and how to
navigate the stack and follow execution, and those skills will get you
pretty far. But there are times when it's not convenient to insert a
call to ``set_trace``, and not practical to step all the way to the
problem point. For example, what if you want to inspect how middleware
is loaded in Django? The solution is *breakpoints*.

A breakpoint is similar to a call to ``set_trace``: when Python
encounters one, it drops into the debugger. But breakpoints can have
conditions associated with them, and can be selectively enabled and
disabled during the run of a program, making them more flexible and
powerful.

Setting Breakpoints
-------------------

A breakpoint is set using the ``break`` command. For example, if we
wanted to stop the program when we load middleware, we'd start the
program, enter PDB, and then set the breakpoint::

  $ ../bin/python -m pdb ../bin/django runserver --settings=pdbdemo.settings --nothreading --noreload
  > /Users/nathan/work/pdb/bin/django(3)<module>()
  -> import sys
  (Pdb) break django/core/handlers/base.py:31
  Breakpoint 1 at /Users/nathan/work/pdb/eggs/Django-1.4.3-py2.7.egg/django/core/handlers/base.py:31
  (Pdb) c
  Validating models...

  0 errors found
  Django version 1.4.3, using settings 'pdbdemo.settings'
  Development server is running at http://127.0.0.1:8000/
  Quit the server with CONTROL-C.

If we access a URL on the test server, we'll see the debugger start::

  > /Users/nathan/work/pdb/eggs/Django-1.4.3-py2.7.egg/django/core/handlers/base.py(31)load_middleware()
  -> from django.conf import settings
  (Pdb)

If we ``cont``\ inue at this point, we'll see Django is ready to serve
requests.

::

  (Pdb) c
  Validating models...

  0 errors found
  Django version 1.4.3, using settings 'pdbdemo.settings'
  Development server is running at http://127.0.0.1:8000/
  Quit the server with CONTROL-C.

When we request a page with the browser, we'll see our breakpoint
triggered. Issuing the ``where`` command, we can see that we're inside
the request handler and ``load_middleware()``.

::

  > /Users/nathan/work/pdb/eggs/Django-1.4.3-py2.7.egg/django/core/handlers/base.py(31)load_middleware()
  -> from django.conf import settings
  (Pdb) where

  ...

    /Users/nathan/work/pdb/eggs/Django-1.4.3-py2.7.egg/django/core/handlers/wsgi.py(219)__call__()
  -> self.load_middleware()
  > /Users/nathan/work/pdb/eggs/Django-1.4.3-py2.7.egg/django/core/handlers/base.py(31)load_middleware()
  -> from django.conf import settings


Note that breakpoints are *thread specific*. This means that when
using the Django ``runserver`` command, you need to disable the
threaded features. ``--nothreading --noreload`` disables the reload
watcher and threading.

.. note::

   A variant of the ``break`` command, ``tbreak``, takes the same
   arguments, but creates a temporary breakpoint, which is cleared
   after the first hit.


If you press Ctrl-C, the program will restart since we're running
under the PDB module. The breakpoint is still active.

::

  (Pdb) break
  Num Type         Disp Enb   Where
  1   breakpoint   keep yes   at /Users/nathan/work/pdb/eggs/Django-1.4.3-py2.7.egg/django/core/handlers/base.py:31
          breakpoint already hit 1 time

You can see that PDB reports how many times the breakpoint has been
triggered.

Toggling Breakpoints
--------------------

The breakpoint number (``1``) above can be used to control its
behavior with the following commands:

* ``disable [bpnum]`` disables the given breakpoint. The breakpoint
  remains set, but will not be triggered when the line is encountered.
* ``enable [bpnum]`` enables the given breakpoint.
* ``clear`` clears the breakpoints specified. If no breakpoints are
  specified, prompt to clear all breakpoints.
* ``ignore bpnum [count]`` will ignore a breakpoint for [count] hits.

Breakpoint Conditions
---------------------

You can also specify a condition for a breakpoint. When the breakpoint
is encountered, the condition is evaluated. If it evaluates True, you
enter the debugger. A condition can be specified as the final argument
to the ``break`` command. It can also be set (or changed) later with
the ``condition`` command.

For example, to set a breakpoint for POST requests in a Django
project::

  $ ../bin/python -m pdb ../bin/django runserver --settings=pdbdemo.settings --nothreading --noreload
  > /home/nathan/p/pdb/bin/django(3)<module>()
  -> import sys
  (Pdb) break django/core/handlers/base.py:82, request.method.lower() == 'post'
  Breakpoint 1 at /home/nathan/p/pdb/eggs/Django-1.4.3-py2.7.egg/django/core/handlers/base.py:82
  (Pdb) break
  Num Type         Disp Enb   Where
  1   breakpoint   keep yes   at /home/nathan/p/pdb/eggs/Django-1.4.3-py2.7.egg/django/core/handlers/base.py:82
          stop only if request.method.lower() == 'post'

The condition follows the module and line number, separated by a
comma, and is evaluated in the context of the breakpoint.

If you make a POST request using ``curl`` after setting the
breakpoint, the breakpoint will trigger. Making a GET request will not
trigger the breakpoint.

::

  (Pdb) c
  Validating models...

  0 errors found
  Django version 1.4.3, using settings 'pdbdemo.settings'
  Development server is running at http://127.0.0.1:8000/
  Quit the server with CONTROL-C.
  > /home/nathan/p/pdb/eggs/Django-1.4.3-py2.7.egg/django/core/handlers/base.py(82)get_response()
  -> urlconf = settings.ROOT_URLCONF
  (Pdb) l
   77  	        try:
   78  	            # Setup default url resolver for this thread, this code is outside
   79  	            # the try/except so we don't get a spurious "unbound local
   80  	            # variable" exception in the event an exception is raised before
   81  	            # resolver is set
   82 B->	            urlconf = settings.ROOT_URLCONF
   83  	            urlresolvers.set_urlconf(urlconf)
   84  	            resolver = urlresolvers.RegexURLResolver(r'^/', urlconf)
   85  	            try:
   86  	                response = None
   87  	                # Apply request middleware
  (Pdb) n
  > /home/nathan/p/pdb/eggs/Django-1.4.3-py2.7.egg/django/core/handlers/base.py(83)get_response()
  -> urlresolvers.set_urlconf(urlconf)
  (Pdb) !request.method
  'POST'
  (Pdb) c
  [08/Jan/2013 22:36:13] "POST /hello/world HTTP/1.1" 200 59


Extending PDB
=============

Aliases
-------

PDB supports defining aliases for actions you take frequently.

::

  alias printdict for key, value in %1.items(): print "%s: %s" % (key, value)

Will create a ``printdict`` command. ``%1`` will replaced by the first
parameter to the command.

Combining Aliases
-----------------

Aliases can reference other aliased commands, allowing you to compose
more powerful commands.

::

  alias cookies printdict getattr(locals().get('request', %1), 'COOKIES')

Breakpoint Command
------------------

PDB also allows you to specify commands to execute when a breakpoint
is triggered. This allows you to automatically execute any PDB command
when a breakpoint is encountered, including things like changing the
ignore count, disabling or enabling other breakpoints, or printing the
value of a variable.

Consider the situation where it'd be helpful to display the value of a
variable when a request comes in: you don't necessarily want to set a
breakpoint, you'd just like to see it in the console as you're
working. You can do this using breakpoint commands.

First, start the program under PDB and set the breakpoint like you
normally would::

  $ ../bin/python -m pdb ../bin/django runserver --settings=pdbdemo.settings --nothreading --noreload
  > /home/nathan/p/pdb/bin/django(3)<module>()
  -> import sys
  (Pdb) break django/core/handlers/base.py:75
  Breakpoint 1 at /home/nathan/p/pdb/eggs/Django-1.4.3-py2.7.egg/django/core/handlers/base.py:75
  (Pdb) break
  Num Type         Disp Enb   Where
  1   breakpoint   keep yes   at /home/nathan/p/pdb/eggs/Django-1.4.3-py2.7.egg/django/core/handlers/base.py:75

Now set the commands to execute on breakpoint 1::

  (Pdb) commands 1
  (com) print request.method
  (com) cont
  (Pdb) break
  Num Type         Disp Enb   Where
  1   breakpoint   keep yes   at
  /home/nathan/p/pdb/eggs/Django-1.4.3-py2.7.egg/django/core/handlers/base.py:75

You can see the prompt changes from ``(Pdb)`` to ``(com)`` when
entering commands. The command entry is terminated when you type
``end`` or any PDB command that resumes execution (``cont`` in this case).

If we continue execution and make a couple requests, we'll see the
``print`` command in action::

  (Pdb) cont
  Validating models...

  0 errors found
  Django version 1.4.3, using settings 'pdbdemo.settings'
  Development server is running at http://127.0.0.1:8000/
  Quit the server with CONTROL-C.
  GET
  > /home/nathan/p/pdb/eggs/Django-1.4.3-py2.7.egg/django/core/handlers/base.py(75)get_response()
  -> from django.conf import settings
  [09/Jan/2013 10:45:50] "GET /hello/world HTTP/1.1" 200 59
  GET
  > /home/nathan/p/pdb/eggs/Django-1.4.3-py2.7.egg/django/core/handlers/base.py(75)get_response()
  -> from django.conf import settings
  [09/Jan/2013 10:45:55] "GET /hello/world HTTP/1.1" 200 59
  POST
  > /home/nathan/p/pdb/eggs/Django-1.4.3-py2.7.egg/django/core/handlers/base.py(75)get_response()
  -> from django.conf import settings
  [09/Jan/2013 10:46:18] "POST /hello/world HTTP/1.1" 200 59

Note that the normal breakpoint message is still printed unless we use
the ``silent`` command in our list of breakpoint commands.

See the `command reference`_ for details.

.pdbrc
------

When PDB starts it looks for a ``.pdbrc`` file in the user's home
directory and the current directory (if both are found, the current
directory file is loaded after the one in the home directory). The
contents of the ``.pdbrc`` is executed as if it'd been typed into the
PDB prompt.

There are two PDB commands that make this particularly powerful.



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
