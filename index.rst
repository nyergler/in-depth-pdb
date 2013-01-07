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

Calling ``settrace`` may be the most common way to enter PDB, but it
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

PDB also has an ``args`` command. XXX

Evaluating Expressions
----------------------

XXX

You can also use the ``print``
statement, but

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


b(reak) [[filename:]lineno | function[, condition]]
With a lineno argument, set a break there in the current file. With a function argument, set a break at the first executable statement within that function. The line number may be prefixed with a filename and a colon, to specify a breakpoint in another file (probably one that hasn’t been loaded yet). The file is searched on sys.path. Note that each breakpoint is assigned a number to which all the other breakpoint commands refer.

If a second argument is present, it is an expression which must evaluate to true before the breakpoint is honored.


cl(ear) [filename:lineno | bpnumber [bpnumber ...]]
With a filename:lineno argument, clear all the breakpoints at this line. With a space separated list of breakpoint numbers, clear those breakpoints. Without argument, clear all breaks (but first ask confirmation).
disable [bpnumber [bpnumber ...]]
Disables the breakpoints given as a space separated list of breakpoint numbers. Disabling a breakpoint means it cannot cause the program to stop execution, but unlike clearing a breakpoint, it remains in the list of breakpoints and can be (re-)enabled.
enable [bpnumber [bpnumber ...]]
Enables the breakpoints specified.
ignore bpnumber [count]
Sets the ignore count for the given breakpoint number. If count is omitted, the ignore count is set to 0. A breakpoint becomes active when the ignore count is zero. When non-zero, the count is decremented each time the breakpoint is reached and the breakpoint is not disabled and any associated condition evaluates to true.
condition bpnumber [condition]
Condition is an expression which must evaluate to true before the breakpoint is honored. If condition is absent, any existing condition is removed; i.e., the breakpoint is made unconditional.


Extending PDB
=============


commands [bpnumber]
Specify a list of commands for breakpoint number bpnumber. The commands themselves appear on the following lines. Type a line containing just ‘end’ to terminate the commands. An example:

(Pdb) commands 1
(com) print some_variable
(com) end
(Pdb)
To remove all commands from a breakpoint, type commands and follow it immediately with end; that is, give no commands.

With no bpnumber argument, commands refers to the last breakpoint set.

You can use breakpoint commands to start your program up again. Simply use the continue command, or step, or any other command that resumes execution.

Specifying any command resuming execution (currently continue, step, next, return, jump, quit and their abbreviations) terminates the command list (as if that command was immediately followed by end). This is because any time you resume execution (even with a simple next or step), you may encounter another breakpoint–which could have its own command list, leading to ambiguities about which list to execute.

If you use the ‘silent’ command in the command list, the usual message about stopping at a breakpoint is not printed. This may be desirable for breakpoints that are to print a specific message and then continue. If none of the other commands print anything, you see no sign that the breakpoint was reached.

New in version 2.5.


alias [name [command]]
Creates an alias called name that executes command. The command must not be enclosed in quotes. Replaceable parameters can be indicated by %1, %2, and so on, while %* is replaced by all the parameters. If no command is given, the current alias for name is shown. If no arguments are given, all aliases are listed.

Aliases may be nested and can contain anything that can be legally typed at the pdb prompt. Note that internal pdb commands can be overridden by aliases. Such a command is then hidden until the alias is removed. Aliasing is recursively applied to the first word of the command line; all other words in the line are left alone.

As an example, here are two useful aliases (especially when placed in the .pdbrc file):

#Print instance variables (usage "pi classInst")
alias pi for k in %1.__dict__.keys(): print "%1.",k,"=",%1.__dict__[k]
#Print instance variables in self
alias ps pi self

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
