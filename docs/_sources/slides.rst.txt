.. role:: strike
    :class: strike

.. highlight:: python

.. rst-class:: content-flexbox content-vcenter dark

.. slide::

   .. rst-class:: slides-link

   ::

     http://presentotron.com/nyergler/pdb


     http://github.com/nyergler/in-depth-pdb

.. rst-class:: segue dark nobackground

PDB: The Python Debugger
========================

.. only:: not slides

   Most developers have a preferred debugging strategy, and many of them
   are variations on the ``print`` statement. There's nothing wrong with
   that, you can get a lot of information about what a program is doing
   by logging or printing information about its state.

   They fall short, however, in that you need to know what you want
   you're looking for before you start: if you realize after seeing
   some data that what you really need to know if the state of some
   other variable, you usually need to change the print statements and
   restart execution.

   Debuggers -- and PDB, in particular -- are a more flexible tool for
   inspecting the state of a running program. PDB is built into
   Python, so if you're using Python, you can already use it.

.. nextslide:: Look around running code

.. only:: not slides

   With PDB you can inspect running code, and see what variables are
   set to.

.. code-block:: none
   :emphasize-lines: 3-4

   > pfcalc.py(28)push()
   -> value = int(value_or_operator)
   (Pdb) p value_or_operator
   'abc'

.. nextslide:: Look around Python's code

.. only:: not slides

   You can also look around code in the Python standard library. For
   example, if you wanted to know what ``os.path.join`` actually does,
   you can stop inside of it and look around. And you can do that
   *without editing the source file*.

..
   (Pdb) b os.path.join
   Breakpoint 2 at /System/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/posixpath.py:68
   (Pdb) c

.. code-block:: none
   :emphasize-lines: 5-7

   >>> os.path.join('/Users', 'nathan')
   > /.../python2.7/posixpath.py(73)join()
   -> path = a
   (Pdb) list
    68 B   def join(a, *p):
    69         """Join two or more pathname components, inserting '/' as needed.
    70         If any component is an absolute path, all previous path components
    71         will be discarded.  An empty last part will result in a path that
    72         ends with a separator."""
    73  ->     path = a
    74         for b in p:
    75             if b.startswith('/'):
    76                 path = b
    77             elif path == '' or path.endswith('/'):
    78                 path +=  b
   (Pdb) !a
   '/Users'
   (Pdb) !p
   ('nathan',)

.. nextslide:: Return to the scene of the crime

.. only:: not slides

   You can also return to the scene of the proverbial crime using the
   post-mortem debugger. This feature of PDB let's you inspect the
   state of your program -- including the call stack -- as it existed
   when a crashing exception occurred.

.. code-block:: none
   :line-classes: 2-12(build-item-1),13-17(build-item-2)
   :emphasize-lines: 1,12,15-16

   >>> s = make_server('', 8000, pfcalc.rpn_app)
   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
     File "/usr/lib/python2.7/wsgiref/simple_server.py", line 144, in make_server
       server = server_class((host, port), handler_class)
     File "/usr/lib/python2.7/SocketServer.py", line 419, in __init__
       self.server_bind()
     File "/usr/lib/python2.7/wsgiref/simple_server.py", line 48, in server_bind
       HTTPServer.server_bind(self)
     File "/usr/lib/python2.7/SocketServer.py", line 430, in server_bind
       self.socket.bind(self.server_address)
   socket.error: [Errno 98] Address already in use
   >>> import pdb
   >>> pdb.pm()
   > /usr/lib/python2.7/socket.py(224)meth()
   -> return getattr(self._sock,name)(*args)
   (Pdb)


.. nextslide:: Everybody Prints
   :classes: dark segue

.. nextslide:: PDB is Better
   :classes: dark segue

.. only:: not slides

   Using ``print`` is great, if you know what you're looking for. PDB
   is better. Reading this will show you how to use it to:

.. rst-class:: build white larger

* Explore the state of a running program. Or a dead one.
* Repeatedly run a program to debug it
* Build the tools you need to extend it

.. rst-class:: segue dark

PDB 101
=======

.. only:: not slides

   Let's start with the most common way people use PDB.

.. rst-class:: content-columns-2 snap

Explicit Trace Points
---------------------

.. only:: not slides

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

.. rst-class:: gutter

.. literalinclude:: /samples/fibonacci_trace.py
   :line-classes: 13(arrow-line)
   :emphasize-lines: 14

.. rst-class:: column-break-before

.. code-block:: none
   :emphasize-lines: 3

   $ python fibonacci_trace.py 5
   > fibonacci_trace.py(12)<module>()
   -> print (fib(int(sys.argv[-1])))
   (Pdb)

PDB stops the program immediately after the trace point.

.. only:: not slides

   The PDB prompt -- ``(Pdb)`` -- shows the path of the current module
   (``fibonacci_trace.py`` here), the line number (``12``), and the
   current line. It also shows the name of the function currently
   being executed, although in this case it's just ``<module>`` since
   we're at module level code.

   At the prompt you can enter one of the `debugger commands`_. You
   can gain a lot of understanding about code by simply following the
   execution path using the ``next`` and ``step`` commands.

.. rst-class:: content-columns-2 snap

``next``
--------

.. rst-class:: gutter

.. literalinclude:: /samples/fibonacci_trace.py
   :emphasize-lines: 14

.. rst-class:: columns-break-before

.. code-block:: none
   :emphasize-lines: 3

   $ python fibonacci_trace.py 5
   > fibonacci_trace.py(14)<module>()
   -> print (fib(sys.argv[-1]))
   (Pdb) next
   8
   --Return--
   > fibonacci_trace.py(14)<module>()->None
   -> print (fib(sys.argv[-1]))
   (Pdb)

``next`` will execute the current line (including any calls it
makes)


.. rst-class:: content-columns-2 snap

``step``
--------

.. rst-class:: gutter

.. literalinclude:: /samples/fibonacci_trace.py
   :emphasize-lines: 3,14

.. rst-class:: columns-break-before

.. code-block:: none
   :emphasize-lines: 3,6

   $ python fibonacci_trace.py 5
   > fibonacci_trace.py(14)<module>()
   -> print (fib(sys.argv[-1]))
   (Pdb) step
   --Call--
   > fibonacci_trace.py(3)fib()
   -> def fib(n):
   (Pdb)

``step`` will stop at the next statement (which may be inside a
function call)


.. rst-class:: content-columns-2 snap


``cont``
--------

.. rst-class:: gutter

.. literalinclude:: /samples/fibonacci_trace.py

.. rst-class:: columns-break-before

.. code-block:: none
   :emphasize-lines: 8

   $ python fibonacci_trace.py 5
   > fibonacci_trace.py(14)<module>()
   -> print (fib(sys.argv[-1]))
   (Pdb) step
   --Call--
   > fibonacci_trace.py(3)fib()
   -> def fib(n):
   (Pdb) cont
   8

``cont`` will leave the debugger and let your program **continue**
executing

PDB 101 Review
--------------

* ``next`` executes the current line
* ``step`` executes the current line, stop ASAP
* ``cont`` continue execution
* Pressing Enter *repeats* previous command

.. rst-class:: tip

Asking for Help
===============

.. only:: not slides

   The PDB prompt isn't the same as a Python prompt: you can do lots
   of Python-like things there, but it has its own rules. It looks
   confusing at first because it's optimized for speed once you know
   how it works. And you can always *ask for help*.

::

   (Pdb) help

   Documented commands (type help <topic>):
   ========================================
   EOF    bt         cont      enable  jump  pp       run      unt
   a      c          continue  exit    l     q        s        until
   alias  cl         d         h       list  quit     step     up
   args   clear      debug     help    n     r        tbreak   w
   b      commands   disable   ignore  next  restart  u        whatis
   break  condition  down      j       p     return   unalias  where

   Miscellaneous help topics:
   ==========================
   exec  pdb

   Undocumented commands:
   ======================
   retval  rv


.. rst-class:: segue dark

Executing Code Under PDB
========================

.. only:: not slides

   Calling ``set_trace`` may be the most common way to enter PDB, but
   it is definitely not the only way. The PDB module provides several
   ways to enter the debugger; we'll look at the main ones, and then
   focus on two.


Running PDB as a Script
-----------------------

.. only:: not slides

   PDB can by run as a Python module using ``-m`` command line parameter
   to Python. In this mode, additional arguments are interpreted as the
   program to run under PDB.

::

   $ python -m pdb samples/fibonacci.py 5
   > fibonacci.py(1)<module>()
   -> import sys
   (Pdb)

.. only:: not slides

   This will drop us into PDB immediately, allowing us to set
   breakpoints, examine initial state, etc. Note that the current line
   is the first ``import`` in the file:: this is because when running
   as a module, PDB stops execution before the program begins.

   When your program ends, it will automatically be restarted for
   another run.

.. nextslide:: Running Django under PDB

It's entirely possible to run your Django app under PDB::

  $ python -m pdb django runserver --settings=pdbdemo.settings

If you want to set a low level breakpoint in your application,
that's a good way to get the PDB console before anything happens.


pdb.run
-------

.. only:: not slides

   The ``pdb`` module provides three ways to directly execute code
   under control of the debugger. These run methods also allow you to
   specify the global and local context for statements and
   expressions. I use these methods far less than other PDB utilities,
   but they're useful for very fine grained testing and introspection.

   ``pdb.run`` and ``pdb.runeval`` execute a Python statement or
   expression, respectively, under control of the debugger. The code
   under test is provided as a string, along with option dictionaries
   specifying the global and local environment.

.. only:: slides

   Execute a statement or expression under the debugger.

::

   >>> import pdb
   >>> pdb.run("fib('25')")
   > <string>(1)<module>()
   (Pdb)

::

   >>> import pdb
   >>> pdb.runcall(fib, 25)
   > fibonacci.py(7)fib()
   -> if n <= 1:
   (Pdb)


.. rst-class:: segue dark

Debugging with PDB
==================

HTTP Maths
----------

Consider a small web application that provides a `postfix notation`_
calculator. You pass your arguments as path elements, and it applies
them to the stack and returns the result.

.. code-block:: none

   $ curl "http://localhost:8000/2/1/+"
   The answer is 3
   $ curl "http://localhost:8000/2/10/*"
   The answer is 20
   curl "http://localhost:8000/2/10/+/2/*"
   The answer is 24

.. nextslide:: HTTP :strike:`Maths` Bugs

It's cool, but not great with unexpected input.

::

   $ curl http://localhost:8000/2/abc/+/

.. code-block:: none
   :emphasize-lines: 11

   Traceback (most recent call last):
     ...
     File "pfcalc_wsgi.py", line 39, in handle
       handler.run(self.server.get_app())
     File "pfcalc_wsgi.py", line 17, in run
       self.result = application(self.environ, self.start_response)
     File "pfcalc.py", line 46, in rpn_app
       c.push(element)
     File "pfcalc.py", line 28, in push
       value = int(value_or_operator)
   ValueError: invalid literal for int() with base 10: 'abc'

.. nextslide:: HTTP :strike:`Maths` Bugs

We can run it under ``pdb`` to see what's actually happening when it
blows up.

::

   python -m pdb pfcalc.py
   > pfcalc.py(1)<module>()
   -> from wsgiref.simple_server import make_server
   (Pdb) cont
   Serving on port 8000...

::

   $ curl http://localhost:8000/2/abc/+

.. nextslide:: HTTP :strike:`Maths` Bugs

Now when we hit the bad URL with ``curl``, Python drops into PDB.

::

   $ curl http://localhost:8000/2/abc/+/

.. rst-class:: build-item-1

.. code-block:: python
   :line-classes: 10-14(build-item-2)

   Traceback (most recent call last):
     ...
     File "pfcalc_wsgi.py", line 17, in run
       self.result = application(self.environ, self.start_response)
     File "pfcalc.py", line 46, in rpn_app
       c.push(element)
     File "pfcalc.py", line 28, in push
       value = int(value_or_operator)
   ValueError: invalid literal for int() with base 10: 'abc'
   Uncaught exception. Entering post mortem debugging
   Running 'cont' or 'step' will restart the program
   > pfcalc.py(28)push()
   -> value = int(value_or_operator)
   (Pdb)


Inspecting State
----------------

.. only:: not slides

   Entering the debugger is only interesting if you can actually use it
   to figure out what's going on in a program, so let's talk about how
   you interact with locals inside of the debugger.

   There are two debugger commands that are useful for inspecting values
   in the debugger:: ``p`` and ``pp`` will print and
   "pretty-print" a value, respectively.

.. only:: slides

    You can ``p``\ rint the value of a variable.

::

   > pfcalc.py(28)push()
   -> value = int(value_or_operator)
   (Pdb) p value_or_operator
   'abc'

You can also look at what arguments were passed to the current
function using ``args``.

::

   (Pdb) args
   self = <__main__.Calculator object at 0x1047bff10>
   value_or_operator = abc

Listing Code
------------

::

   (Pdb) list
    23  	            value = self.OPERATORS[value_or_operator](
    24  	                self.state.pop(),
    25  	                self.state.pop(),
    26  	            )
    27  	        else:
    28  ->	            value = int(value_or_operator)
    29
    30  	        self.state.append(value)
    31
    32  	    def result(self):
    33

.. You can also give it additional parameters to control what lines are shown.

.. nextslide::
   :classes: content-columns-2

.. rst-class:: span-columns

Python 3.2 added the long list (``ll``) command, which lets you see
the entire function.

.. code-block:: none

   (Pdb) list



    22             value = self.OPERATORS[value_or_operator](
    23                 self.state.pop(),
    24                 self.state.pop(),
    25             )
    26         else:
    27  ->         value = int(value_or_operator)
    28
    29         self.state.append(value)
    30
    31     def result(self):
    32

.. code-block:: none

   (Pdb) ll
    19     def push(self, value_or_operator):
    20
    21         if value_or_operator in self.OPERATORS:
    22             value = self.OPERATORS[value_or_operator](
    23                 self.state.pop(),
    24                 self.state.pop(),
    25             )
    26         else:
    27  ->         value = int(value_or_operator)
    28
    29         self.state.append(value)


Pretty Print
------------

You can pretty print the value of a variable using the ``pp`` command.

::

   (Pdb) p self.OPERATORS
   {'*': <slot wrapper '__mul__' of 'int' objects>, '+': <slot wrapper '__add__' of 'int' objects>, '/': <slot wrapper '__div__' of 'int' objects>}

::

   (Pdb) pp self.OPERATORS
   {'*': <slot wrapper '__mul__' of 'int' objects>,
    '+': <slot wrapper '__add__' of 'int' objects>,
    '/': <slot wrapper '__div__' of 'int' objects>}



Evaluating Expressions
----------------------

You can also evaluate expressions using the ``!`` command.

.. only:: not slides

   Most PDB commands have a short and long form. For example, ``next``
   can be abbreviated as ``n``. Check the `debugger command`_
   reference for details.

   Note that this short form is a good reason to use ``!`` to denote
   Python expressions: input that could either be an expression or a
   debugger command is evaluated as the latter. It's frustrating to
   expect to evaluate a variable named ``c`` and wind up exiting the
   debugger and continuing instead.

.. rst-class:: build-item-1

.. literalinclude:: /samples/add.py
   :pyobject: add

.. rst-class:: build-item-2

.. code-block:: none
   :line-classes: 3-5(build-item-3),6-7(build-item-4)

   > add.py(5)add()
   -> return a + b + c
   (Pdb) b+c
   *** The specified object '+c' is not a function
   or was not found along sys.path.
   (Pdb) !b+c
   5

.. nextslide::

.. only:: not slides

   .. admonition:: ``interact``

      New in Python 3.2, the ``interact`` command gives you an
      interactive prompt with the same locals and globals as the current
      position. This makes it easier to evaluate expressions and explore
      the current position in the code.

.. only:: slides

   Python 3.2 added the ``interact`` command

::

   (Pdb) interact
   *interactive*
   >>> locals().keys()
   dict_keys(['make_server', 'self', 'httpd', '__name__', '__builtins__', 'CalculatorWSGIHandler', '__file__', 'value_or_operator', 'CalculatorServer', 'Calculator', 'rpn_app'])
   >>>


.. rst-class:: segue dark

Navigating Execution
====================

.. nextslide::

Let's consider another example where our calculator isn't so hot.

::

   $ curl http://localhost:8000/2/3/+/5


.. rst-class:: build-item-1

.. code-block:: none

   Traceback (most recent call last):
     ...
     File "/System/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/SocketServer.py", line 649, in __init__
       self.handle()
     File "pfcalc_wsgi.py", line 17, in run
       self.result = application(self.environ, self.start_response)
     File "pfcalc.py", line 54, in rpn_app
       "The answer is %d" % (c.result(),),
     File "pfcalc.py", line 36, in result
       raise SyntaxError("Invalid expression.")
   SyntaxError: Invalid expression.
   > pfcalc.py(36)result()
   -> raise SyntaxError("Invalid expression.")
   (Pdb)


Where am I?
-----------

.. only:: not slides

   Once inside the debugger, it's useful to be able to figure out
   where you are in the call stack. The ``where`` command prints the
   stack trace with the most recent call last.

The ``where`` command shows the call stack that got us into this mess.

.. code-block:: none
   :line-classes: 2-(build-item-1)

   (Pdb) where
     /System/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/pdb.py(1314)main()
   -> pdb._runscript(mainpyfile)
     /System/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/bdb.py(400)run()
   -> exec cmd in globals, locals
     /System/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/SocketServer.py(238)serve_forever()
   -> self._handle_request_noblock()
     pfcalc_wsgi.py(39)handle()
   -> handler.run(self.server.get_app())
     pfcalc_wsgi.py(17)run()
   -> self.result = application(self.environ, self.start_response)
     pfcalc.py(54)rpn_app()
   -> "The answer is %d" % (c.result(),),
   > pfcalc.py(36)result()
   -> raise SyntaxError("Invalid expression.")
   (Pdb)

Navigating the Stack
--------------------

You can use the ``up`` command to move one frame up the stack.

::

   (Pdb) up
   > pfcalc.py(54)rpn_app()
   -> "The answer is %d" % (c.result(),),

PDB shows that the current position is now the call to ``result``.

.. nextslide::

Other PDB commands operate in the context of the current position.

::

   (Pdb) list
    49  	    headers = [('Content-type', 'text/plain')]
    50
    51  	    start_response(status, headers)
    52
    53  	    return [
    54  ->	        "The answer is %d" % (c.result(),),
    55  	    ]
    56
    57
   (Pdb)


.. rst-class:: segue dark

Post-Mortem Debugging
=====================

.. nextslide::

We've been running the server using the PDB module::

  $ python -m pdb pfcalc.py

.. only:: not slides

   Executing your program using the ``pdb`` module uses the *post-mortem*
   debugger. The post-mortem debugger uses ``sys.last_exception`` to
   figure out where to start debugging.

.. nextslide::

Our server starts with the following lines:

.. code-block:: python

   httpd = make_server('',
       8000, rpn_app,
       server_class=CalculatorServer,
       handler_class=CalculatorWSGIHandler,
   )
   print "Serving on port 8000..."
   httpd.serve_forever()

.. nextslide::
   :classes: content-columns-2

.. rst-class:: span-columns

The post-mortem debugger acts as a top-level exception handler.

.. code-block:: python

   httpd = make_server('',
       8000, rpn_app,
       server_class=CalculatorServer,
       handler_class=CalculatorWSGIHandler,
   )
   print "Serving on port 8000..."
   httpd.serve_forever()

.. code-block:: python

   try:
     httpd = make_server('',
         8000, rpn_app,
         server_class=CalculatorServer,
         handler_class=CalculatorWSGIHandler,
     )
     print "Serving on port 8000..."
     httpd.serve_forever()
   except:
     import pdb

     # debug the exception being handled
     pdb.post_mortem()

.. nextslide::

You can imagine writing this using an explicit ``set_trace()``
instead.

::

  try:
    httpd = make_server('', 8000, rpn_app,
                        server_class=CalculatorServer,
                        handler_class=CalculatorWSGIHandler,
    )
    print "Serving on port 8000..."
    httpd.serve_forever()
  except:
    import pdb
    pdb.set_trace()

.. nextslide::

If we run this version of the server and trigger an error, the
difference will be obvious.

::

   $ curl http://localhost:8000/2/3/+/5

::

   $ python pf_settrace.py
   --Return--
   > pf_settrace.py(15)<module>()->None
   -> pdb.set_trace()
   (Pdb)

.. only:: not slides

   As you can see, when ``set_trace`` enters the debugger, you don't have
   any of the exception context. The error has already happened, and
   you're too late. ``set_trace`` is useful when you want to pause
   execution and look around, but not when you're catching an exception.


.. rst-class:: segue dark

Breakpoints
===========

.. only:: not slides

   So far we've primarily looked at entering the debugger explicitly
   (``set_trace``) and invoking the post-mortem debugger on exception
   (``python -m pdb``). Of course it'd be nice to start the debugger
   *before* we run into trouble.

   **PDB breakpoints let you enter the debugger at a specific point
   without modifying the source code.**

.. rst-class:: content-columns-2

Setting Breakpoints
-------------------

.. only:: not slides

   A breakpoint is set using the ``break`` command. For example, if we
   want to inspect the path handling portion of our calculator, we might
   want to enter the debugger when ``rpn_app`` is called:

.. literalinclude:: /samples/pfcalc.py
   :pyobject: rpn_app
   :emphasize-lines: 1

.. only:: not slides

   We can do this with a breakpoint.

.. code-block:: bash
   :emphasize-lines: 4

   $ python -m pdb pfcalc.py
   > pfcalc.py(1)<module>()
   -> from wsgiref.simple_server import make_server
   (Pdb) break pfcalc.rpn_app
   Breakpoint 1 at pfcalc.py:41

.. rst-class:: content-columns-2

Setting Breakpoints
-------------------

.. literalinclude:: /samples/pfcalc.py
   :pyobject: rpn_app
   :emphasize-lines: 1

.. code-block:: bash
   :emphasize-lines: 4

   $ python -m pdb pfcalc.py
   > pfcalc.py(1)<module>()
   -> from wsgiref.simple_server import make_server
   (Pdb) break pfcalc.py:41
   Breakpoint 1 at pfcalc.py:41
   (Pdb) cont

.. rst-class:: span-columns

   You can also give it a filename and a line number.

   Note that we then exit the debugger by telling it to ``cont``\ inue.

.. nextslide::
   :classes: content-flexbox content-vcenter content-big-example

.. only:: not slides

   The ``break`` command takes an argument which tells it where to break.
   In this case it's a ``module.callable`` dotted path. It prints out
   where the breakpoint was set, and the breakpoint number (**1** in this
   example).

::

   (Pdb) help break
   b(reak) ([file:]lineno | function) [, condition]


.. nextslide::

If we make a request to our application, we'll see it drop into PDB.

::

   $ curl http://localhost:8000/2/3/+

.. rst-class:: build-item-1

::

   > pfcalc.py(43)rpn_app()
   -> c = Calculator()
   (Pdb) n
   > pfcalc.py(45)rpn_app()
   (Pdb) !environ['PATH_INFO']
   '/2/3/+'

.. nextslide::

Issuing the ``break`` command without any arguments will report on the
defined breakpoints::

  (Pdb) break
  Num Type         Disp Enb   Where
  1   breakpoint   keep yes   at pfcalc.py:41
          breakpoint already hit 1 times


.. only:: not slides

   Note that breakpoints are *thread specific*. This means that when
   using the Django ``runserver`` command, you need to disable the
   threaded features. ``--nothreading --noreload`` disables the reload
   watcher and threading.

   .. note::

      A variant of the ``break`` command, ``tbreak``, takes the same
      arguments, but creates a temporary breakpoint, which is cleared
      after the first hit.

.. nextslide::

If you press Ctrl-C, the program will restart since we're running
under the PDB module. The breakpoint is still active.

::

   (Pdb) break
   Num Type         Disp Enb   Where
   1   breakpoint   keep yes   at pfcalc.py:41
           breakpoint already hit 4 times


Manipulating Breakpoints
------------------------

The breakpoint number (``1``) above can be used to control its
behavior with the following commands:

* ``disable [bpnum]``

  Disables the given breakpoint. The breakpoint remains set, but will
  not be triggered when the line is encountered.

* ``enable [bpnum]``

  Enables the given breakpoint.

* ``ignore bpnum [count]``

  Ignore a breakpoint for [count] hits.

* ``clear [bpnum]``

  Clears the breakpoints specified. If no breakpoints are specified,
  prompt to clear all breakpoints.

.. rst-class:: content-flexbox content-vcenter content-big-example

Breakpoint Conditions
---------------------

.. only:: not slides

   You may have noticed that the ``break`` command has this optional
   ``condition`` parameter at the end.

::

   (Pdb) help break
   b(reak) ([file:]lineno | function) [, condition]

.. only:: not slides

   You can also specify a condition for a breakpoint. When the breakpoint
   is encountered, the condition is evaluated. If it evaluates True, you
   enter the debugger. A condition can be specified as the final argument
   to the ``break`` command. It can also be set (or changed) later with
   the ``condition`` command.

.. nextslide::

.. only:: not slides

   Our calculator expects that it will receive GET requests, and we
   can place a breakpoint that only fires when it gets something else.

.. code-block:: none
   :emphasize-lines: 4

   $ python -m pdb pfcalc.py
   > pfcalc.py(1)<module>()
   -> from wsgiref.simple_server import make_server
   (Pdb) break pfcalc.rpn_app, environ['REQUEST_METHOD'] != 'GET'
   Breakpoint 1 at pfcalc.py:40
   (Pdb)

.. nextslide::

.. code-block:: none
   :emphasize-lines: 6-9

   $ python -m pdb pfcalc.py
   > pfcalc.py(1)<module>()
   -> from wsgiref.simple_server import make_server
   (Pdb) break pfcalc.rpn_app, environ['REQUEST_METHOD'] != 'GET'
   Breakpoint 1 at pfcalc.py:40
   (Pdb) break
   Num Type         Disp Enb   Where
   1   breakpoint   keep yes   at pfcalc.py:40
           stop only if environ['REQUEST_METHOD'] != 'GET'
   (Pdb) cont
   Serving on port 8000...

.. nextslide::
   :classes: content-columns-2

.. code-block:: none
   :line-classes: 4(build-item-1),5(build-item-2),6-9(build-item-3),10-11(build-item-4)

   $ python -m pdb pfcalc.py
   ...
   Serving on port 8000...
   127.0.0.1 - - [12/Mar/2014 12:52:24] "GET /2/3/* HTTP/1.1" 200 15
   127.0.0.1 - - [12/Mar/2014 12:52:30] "GET /2/3/+ HTTP/1.1" 200 15
   > pfcalc.py(42)rpn_app()
   -> c = Calculator()
   (Pdb) environ['REQUEST_METHOD']
   'POST'
   (Pdb) cont
   127.0.0.1 - - [12/Mar/2014 12:52:54] "POST /2/3/+ HTTP/1.1" 200 15

.. code-block:: bash
   :line-classes: 1-2(build-item-1),3-4(build-item-2),5(build-item-3),6(build-item-4)

   $ curl http://localhost:8000/2/3/\*
   The answer is 6
   $ curl http://localhost:8000/2/3/+
   The answer is 5
   $ curl http://localhost:8000/2/3/+ -d foo
   The answer is 5

..
   .. nextslide::

     $ ../bin/python -m pdb ../bin/django runserver --settings=pdbdemo.settings --nothreading --noreload
     > /home/nathan/p/pdb/bin/django(3)<module>()
     -> import sys
     (Pdb) break django/core/handlers/base.py:82, request.method.lower() == 'post'
     Breakpoint 1 at /home/nathan/p/pdb/eggs/Django-1.4.3-py2.7.egg/django/core/handlers/base.py:82
     (Pdb) break
     Num Type         Disp Enb   Where
     1   breakpoint   keep yes   at /home/nathan/p/pdb/eggs/Django-1.4.3-py2.7.egg/django/core/handlers/base.py:82
             stop only if request.method.lower() == 'post'


.. rst-class:: segue dark

Extending PDB
=============

Aliases
-------

Define aliases for frequently used commands.


::

  alias dr pp dir(%1)

.. rst-class:: build-item-1

.. code-block:: none
   :emphasize-lines: 3
   :line-classes: 3-(build-item-2)

   (Pdb) p self
   <__main__.Calculator object at 0x7eff1e054790>
   (Pdb) dr self
   ['OPERATORS',
    '__class__',
    '__dict__',
    '__hash__',
    '__init__',
    '__new__',
    '__repr__',
    '__str__',
    'push',
    'result',
    'state']

.. nextslide::

::

  alias loc locals().keys()

.. rst-class:: build-item-1

::

   (Pdb) loc
   ['status', 'c', 'start_response', 'element', 'headers', 'environ']

.. nextslide::

::

  alias printdict for key, value in %1.items(): print "%s: %s" % (key, value)
  alias pd printdict

* Aliases can refer to other aliases
* Arguments are always passed on

.. only:: not slides

   Will create a ``printdict`` command. ``%1`` will replaced by the first
   parameter to the command.

Combining Aliases
-----------------

Aliases can reference other aliased commands, allowing you to compose
more powerful commands.

::

  alias cookies printdict getattr(locals().get('request', %1), 'COOKIES')

Breakpoint Commands
-------------------

.. only:: not slides

   PDB also allows you to specify commands to execute when a breakpoint
   is triggered. This allows you to automatically execute any PDB command
   when a breakpoint is encountered, including things like changing the
   ignore count, disabling or enabling other breakpoints, or printing the
   value of a variable.

   Consider the situation where it'd be helpful to display the value of a
   variable when a request comes in: you don't necessarily want to set a
   breakpoint, you'd just like to see it in the console as you're
   working. You can do this using breakpoint commands.

.. only:: slides

   * PDB can execute debugger commands when a breakpoint is encountered
   * These commands can be anything you normally enter at the ``(Pdb)``
     prompt
   * The command list ends with either the ``end`` command, or any
     command that resumes execution (``step``, ``next``, ``cont``)

.. nextslide::

.. only:: not slides

   First, start the program under PDB and set the breakpoint like you
   normally would:

.. code-block:: none
   :emphasize-lines: 4

   $ python -m pdb pfcalc.py
   > pfcalc.py(1)<module>()
   -> from wsgiref.simple_server import make_server
   (Pdb) break pfcalc.py:21
   Breakpoint 1 at pfcalc.py:21

.. nextslide::

.. only:: not slides

   Now set the commands to execute when breakpoint ``1`` is hit:

.. code-block:: none
   :emphasize-lines: 6,9
   :line-classes: 10-11(build-item-1)

   $ python -m pdb pfcalc.py
   > pfcalc.py(1)<module>()
   -> from wsgiref.simple_server import make_server
   (Pdb) break pfcalc.py:21
   Breakpoint 1 at pfcalc.py:21
   (Pdb) commands 1
   (com) pp self.state
   (com) pp value_or_operator
   (com) cont
   (Pdb) cont
   Serving on port 8000...

.. only:: not slides

   You can see the prompt changes from ``(Pdb)`` to ``(com)`` when
   entering commands. The command entry is terminated when you type
   ``end`` or any PDB command that resumes execution (``cont`` in this
   case).

.. nextslide::
   :classes: content-columns-2

.. only:: not slides

   If we continue execution and make a couple requests, we'll see the
   commands in action.

.. code-block:: none
   :emphasize-lines: 4-5,8-9,12-13
   :line-classes: 4-7(build-item-1),8-11(build-item-2),12-(build-item-3)

   $ python -m pdb pfcalc.py
   ...
   Serving on port 8000...
   []
   '2'
   > pfcalc.py(21)push()
   -> if value_or_operator in self.OPERATORS:
   [2]
   '3'
   > pfcalc.py(21)push()
   -> if value_or_operator in self.OPERATORS:
   [2, 3]
   '*'
   > pfcalc.py(21)push()
   -> if value_or_operator in self.OPERATORS:
   127.0.0.1 - - [12/Mar/2014 12:38:42] "GET /2/3/* HTTP/1.1" 200 15

.. code-block:: bash
   :line-classes: 2(build-item-3)

   $ curl http://localhost:8000/2/3/\*
   The answer is 6

.. only:: not slides

   Note that the normal breakpoint message is still printed unless we
   use the ``silent`` command in our list of breakpoint commands.

   See the `command reference`_ for details.

.pdbrc
------

.. only:: not slides

   When PDB starts it looks for a ``.pdbrc`` file in the user's home
   directory and the current directory (if both are found, the current
   directory file is loaded after the one in the home directory). The
   contents of the ``.pdbrc`` is executed as if it'd been typed into the
   PDB prompt.

.. literalinclude:: pdbrc
   :lines: 1-6

.. only:: slides

   * ``.pdbrc`` will be loaded from your home directory *and* current
     directory
   * Executed line by line in PDB
   * Define aliases, common breakpoints, etc at startup
   * Comments can be included with ``#``

step-watch
----------

Python expressions + PDB commands

.. literalinclude:: pdbrc
   :lines: 7-

Credit: http://stackoverflow.com/questions/7668979/how-do-you-watch-a-variable-in-pdb

See Also
========

* ipdb_: Drop-in replacement for PDB that provides syntax
  highlighting and tab completion
* rdb_: PDB over a socket
* pudb_: Full screen, console debugger
* `pdb++`_: Overrides PDB with some advanced functionality like
  watches
* `wdb`_: PDB over WebSockets
* ``pdbtrack`` is included with modern distributions of
  `python-mode`_, and allows Emacs to open files as they're debugged
  by PDB.

.. only:: not slides

  Recent versions add support for `filename mapping`_ which is
  useful when debugging in a SSH session (ie, Eventbrite's
  vagrant-based setup).

  * `Tracing Python Code
    <http://www.dalkescientific.com/writings/diary/archive/2005/04/20/tracing_python_code.html>`_
  * `Watchpoints in Python <http://sourceforge.net/blog/watchpoints-in-python/>`_

So remember...
==============

* PDB lets you explore your program
* You can stop in code you can't edit
* PDB is an extensible tool

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
.. _`postfix notation`: http://en.wikipedia.org/wiki/Postfix_notation
.. _`pdb++`: https://pypi.python.org/pypi/pdbpp/
.. _`wdb`: https://github.com/Kozea/wdb
