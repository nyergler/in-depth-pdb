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

Getting Started
===============

``pdb`` is a module that ships with Python, and so is included with
any deployment. The most basic way to use it is to import the module
and call ``set_trace()``::

   import pdb; pdb.set_trace()

``set_trace`` instructs Python to drop into the debugger at that
point. For example, if we have the following function defined in
``funcs.py``:

.. literalinclude:: ./pdbdemo/pdbdemo/funcs.py
   :pyobject: calc_sum
   :linenos:


If we add the following line after line 3 (``result = 0``)::

  import pdb; pdb.set_trace()

When ``calc_sum()`` is called, the debugger will start at the ``set_trace``::

  >>> from funcs import calc_sum
  >>> calc_sum(1, 2, 3)
  > /home/nathan/p/pdb/funcs.py(7)calc_sum()
  -> for a in args:
  (Pdb)

The PDB prompt -- ``(Pdb)`` -- shows the next command that will be
executed, in this case ``for a in args:``, along with the filename
(``funcs.py``), line number (``7``), and the function currently being
executed (``calc_sum``).

At the prompt you can enter one of the `debugger commands`_ or
evaluate a Python expression, such as a local variable::

  (Pdb) !result
  0

The continue (``cont``) command will exit the debugger and continue
normal execution::

  (Pdb) cont
  6
  >>>

In this case continuing execution results in the ``calc_sum`` function
completing, and the result (``6``) being printed.

.. sidebar:: Trace Functions & Debuggers

   So what is Python and the PDB module doing when you call
   ``set_trace()``? CPython supports setting a system trace function,
   which supports the implementation of debuggers and other source
   analysis tools in Python itself. A trace function is registered for a
   specific thread, and is called when a stack frame is executed. Trace
   functions are registered using ``sys.settrace``, and provide quite a
   bit of flexibility for introspecting what happens when a program is
   running.

   See the `sys.settrace`_ documentation for details about writing a
   trace function.

Invoking PDB
============

Calling ``set_trace`` may be the most common way to enter PDB, but it
is definitely not the only way. The PDB module provides several ways
to enter the debugger; we'll look at the main ones, and then focus on
two.

python -m pdb
-------------

PDB can by run as a Python module using ``-m`` command line parameter
to Python. In this mode, additional arguments are interpreted as the
program to run under PDB. For example, if we add a ``__main__``
function to our ``funcs.py`` file::

  if __name__ == '__main__':

      print calc_sum(*range(0, 10))

We can execute it with PDB::

  $ python -m pdb funcs.py

This will drop us into PDB immediately, allowing us to set
breakpoints, examine initial state, etc::

  $ ./bin/python -m pdb funcs.py
  > /Users/nathan/work/pdb/funcs.py(1)<module>()
  -> def calc_sum(*args):
  (Pdb)

Note that the "next" frame to be executed is the ``calc_sum`` function
definition: this is because when running as a module, PDB stops
execution before the program begins. If we type ``next`` to go to the
next frame, you'll see that it jumps over the function body to
``__main__`` block.

::

  (Pdb) next
  > /Users/nathan/work/pdb/funcs.py(11)<module>()
  -> if __name__ == '__main__':
  (Pdb)

This makes sense when you remember that function
declarations are executed on import, and bodies are executed on call.

When your program ends, it will automatically be restarted for another run.

.. sidebar:: Running Django under PDB

   It's entirely possible to run your Django app under PDB::

     $ python -m pdb django runserver --settings=pdbdemo.settings

   If you want to set a low level breakpoint in your application,
   that's a good way to get the PDB console before anything happens.

pdb.set_trace
-------------

We've already seen the most common entry to PDB in action,
``set_trace()``. Calling ``set_trace()`` enters the debugger
immediately.

pdb.run
-------

The ``pdb`` module provides three ways to directly execute code under
control of the debugger. These run methods also allow you to specify
the global and local context for statements and expressions. I use
these methods far less than other PDB utilities, but they're useful
for very fine grained testing and introspection.

``pdb.run`` and ``pdb.runeval`` execute a Python statement or
expression, respectively, under control of the debugger. The code
under test is provided as a string, along with option dictionaries
specifying the global and local environment.

The ``next`` command isn't very useful inside of a ``run`` call::

  >>> pdb.run("funcs.calc_sum(1, 2, 3)")
  > <string>(1)<module>()
  (Pdb) next
  --Return--
  > <string>(1)<module>()->None
  (Pdb)
  >>>

The ``--Return--`` call indicates the debugger is returning from a
call, in this case our call to ``funcs.calc_sum``. Because there's only the
one statement to execute, you usually want to ``step`` into the
statement when using this approach::

  >>> pdb.run("funcs.calc_sum(1, 2, 3)")
  > <string>(1)<module>()->None
  (Pdb) step
  --Call--
  > /Users/nathan/work/pdb/funcs.py(1)calc_sum()
  -> def calc_sum(*args):
  (Pdb)

``step`` differs from ``next`` in that step stops inside a called
function, while next executes called functions at (nearly) full speed,
only stopping at the next line in the current function.

``pdb.runcall`` takes a callable as the first argument, followed by
any arguments and keyword arguments.

::

  >>> import pdb
  >>> import funcs
  >>> pdb.runcall(funcs.calc_sum, 1, 2, 3)
  > /Users/nathan/work/pdb/funcs.py(3)calc_sum()
  -> result = 0
  (Pdb) cont
  6
  >>>

pdb.post_mortem
---------------

PDB also provides a post-mortem debugger, which is useful for
debugging code that's already crashed. Consider the following addition
to ``funcs.py``:

.. literalinclude:: ./pdbdemo/pdbdemo/funcs.py
   :pyobject: product_inverses

This function calculates the product of the inverses of a series of
numbers. But it has a problem::

   >>> import funcs
   >>> funcs.product_inverses((1, 2, 3))
   0.16666666666666666
   >>> funcs.product_inverses((1, 2, 3, 0))
   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
     File "funcs.py", line 16, in product_inverses
       result = result * (1.0 / i)
   ZeroDivisionError: float division by zero
   >>>

This is obviously a contrived example, but imagine that this exception
was raised by code that you were calling and didn't have good
visibility into. The post-mortem debugger lets you enter the debugger
at the point an exception occurred.

::

  >>> import pdb;pdb.pm()
  > /Users/nathan/work/pdb/./pdbdemo/pdbdemo/funcs.py(16)product_inverses()
  -> result = result * (1.0 / i)
  (Pdb)

Note that calling ``pdb.pm()`` relies on ``sys.last_traceback`` being
set. `sys.lasttraceback`_ is set whenever Python encounters an
unhandled exception.

There's a variant of the post-mortem call that you can use within an
exception handler. Consider the following variant of our
``product_inverses`` function:

.. literalinclude:: ./pdbdemo/pdbdemo/funcs.py
   :pyobject: try_product_inverses

If we call this version of the function, we'll see the post-mortem
debugger in action::

  >>> import funcs
  >>> funcs.try_product_inverses((0,1,2,3))
  > /Users/nathan/work/pdb/funcs.py(27)try_product_inverses()
  -> result = result * (1.0 / i)
  (Pdb)

The interesting thing to note here is that the next frame for PDB is
where the error actually occurred, **not** where the debugger was
called. Try replacing the call to ``post_mortem`` with a call to
``set_trace`` to see the difference.


Interacting with Locals
=======================

Entering the debugger is only interesting if you can actually use it
to figure out what's going on in a program, so let's talk about how
you interact with locals inside of the debugger.

There are two debugger commands that are useful for inspecting values
in the debugger:: ``p`` and ``pp`` will print and
"pretty-print" a value, respectively.

::

  >>> import funcs
  >>> funcs.try_product_inverses((0, 1, 2, 3))
  > /Users/nathan/work/pdb/funcs.py(27)try_product_inverses()
  -> result = result * (1.0 / i)
  (Pdb) p result
  1.0
  (Pdb) pp result
  1.0
  (Pdb)

Not that interesting for floats, but when examining dictionaries or
other larger data structures, the ``pp`` command can be very useful.

::

  (Pdb) pp locals()
  {'i': 0,
   'ints': (0, 1, 2, 3),
   'pdb': <module 'pdb' from '/System/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/pdb.pyc'>,
   'result': 1.0}
  (Pdb)

PDB also has an ``args`` command that will output the arguments passed
to the current function.


Evaluating Expressions
----------------------

.. XXX

.. You can also use the ``print``
.. statement, but

.. Modifying Values
.. ----------------

.. If you evaluate arbitrary expressions, you may be wondering if you can
.. modify values in place. You can, but keep in mind that there may be
.. unintended side effects. For example, if your code stores references
.. to immutable values, reassigning a variable will create a new instance

.. sidebar:: Command Shortcuts

   Most PDB commands have a short and long form. For example, ``next``
   can be abbreviated as ``n``. Check the `debugger command`_
   reference for details.

   Note that this short form is a good reason to use ``!`` to denote
   Python expressions: input that could either be an expression or a
   debugger command is evaluated as the latter. It's frustrating to
   expect to evaluate a variable named ``c`` and wind up exiting the
   debugger and continuing instead.


Navigating the Stack
====================

Once inside the debugger, it's useful to be able to figure out where
you are in the call stack. The ``where`` command prints the stack
trace with the most recent call last.

You can move up and down the call stack with the ``up`` and ``down``
commands. These are oriented the same was as the output of ``where``:
``up`` moves to an earlier frame, ``down`` to a later frame.

Finally, while the PDB prompt contains the next line that will be
executed, it's often useful to see that line in context. The ``list``
command will display the 11 lines of code around the current line (5
previous, 5 after). You can optionally specify a range to display
more; see the `command reference`_ for details.


Following Execution
===================

We've already seen examples of stepping into code (the ``step``
command) and executing the next frame at the current level (``next``).
Both ``step`` and ``next`` execute the current line; the difference is
that ``step`` stops at the first possible occasion, which may be in
the function called. ``next`` executes the next line and stops when it
is complete.

Occasionally you'll ``step`` when you wanted to ``next``, and wind up
at a lower level than you want to be at. The ``return`` command is
great for this case (or when you've realized that the current function
is uninteresting, not the culprit, etc). ``return`` continues
execution until the current function returns.

There are times when you start debugging an application and want to
skip over some block of code: a loop that will take a while to run,
etc. For example, if you broke into the ``hello`` view at the
beginning of the function, you might want to jump over calculation of
the name.

.. literalinclude:: ./pdbdemo/helloworld/views.py
   :pyobject: hello
   :linenos:

You can use the ``until`` command to continue execution until the
program reaches the given line number.

::
  > /Users/nathan/work/pdb/pdbdemo/helloworld/views.py(8)hello()
  -> name = None
  (Pdb) u 15
  u 15
  > /Users/nathan/work/pdb/eggs/Django-1.4.3-py2.7.egg/django/core/handlers/base.py(111)get_response()
  -> response = callback(request, *callback_args, **callback_kwargs)
  (Pdb)

You can also jump over parts of the code using the cunningly named
``jump`` command.

::

  > /Users/nathan/work/pdb/pdbdemo/helloworld/views.py(8)hello()
  -> name = None
  (Pdb) j 15
  j 15
  > /Users/nathan/work/pdb/pdbdemo/helloworld/views.py(15)hello()
  -> return render_to_response(
  (Pdb) c
  c
  [08/Jan/2013 17:03:49] "GET /hello/world/ HTTP/1.1" 500 57888

The `command reference`_ points out that "not all jumps are allowed —
for instance it is not possible to jump into the middle of a for loop
or out of a finally clause." I don't find many uses for jumps, but
your mileage may vary.

Finally, the ``cont``\ inue command continues execution until the next
breakpoint or trace is encountered.


Setting Breakpoints
===================

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

PDB is pretty powerful on its own, but there are also ways to
customize it: add commands, set default behavior, etc. As an example,
ipdb_, a drop-in replacement that provides syntax highlighting and tab
completion, simply subclasses the ``Pdb`` class.

.pdbrc
------

When PDB starts it looks for a ``.pdbrc`` file in the user's home
directory and the current directory (if both are found, the current
directory file is loaded after the one in the home directory). The
contents of the ``.pdbrc`` is executed as if it'd been typed into the
PDB prompt.

There are two PDB commands that make this particularly powerful.

The ``alias`` command allows you to alias a new command to some PDB
statement. For example::

  alias printdict for key, value in %1.items(): print "%s: %s" % (key, value)

Will create a ``printdict`` command. ``%1`` will replaced by the first
parameter to the command. Aliases can reference other aliased
commands, allowing you to compose more powerful commands.

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

Other Tools
===========

* ipdb_ is a drop-in replacement for PDB that provides syntax
  highlighting, tab completion, and better introspection.
* rdb_
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
