Interacting with Running Code
=============================

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
