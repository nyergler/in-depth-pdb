.. highlight:: python

.. rst-class:: segue dark nobackground

PDB: The Python Debugger
========================

Look around your code
---------------------

XXX Example of inspecting locals

.. rst-class:: content-smaller

Look around Python's code
-------------------------

.. code-block:: none
   :emphasize-lines: 5-7

   (Pdb) b os.path.join
   Breakpoint 2 at /System/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/posixpath.py:68
   (Pdb) c
   >>> os.path.join('/Users', 'nathan')
   > /System/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/posixpath.py(73)join()
   -> path = a
   (Pdb) l
    68 B	def join(a, *p):
    69  	    """Join two or more pathname components, inserting '/' as needed.
    70  	    If any component is an absolute path, all previous path components
    71  	    will be discarded.  An empty last part will result in a path that
    72  	    ends with a separator."""
    73  ->	    path = a
    74  	    for b in p:
    75  	        if b.startswith('/'):
    76  	            path = b
    77  	        elif path == '' or path.endswith('/'):
    78  	            path +=  b
   (Pdb) !a
   '/Users'
   (Pdb) !p
   ('nathan',)
   (Pdb)

Return to the scene of the crime
--------------------------------

.. code-block:: none

   >>> s = make_server('', 8000, pfcalc.rpn_app)
   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
     File "/usr/lib/python2.7/wsgiref/simple_server.py", line 144, in make_server
       server = server_class((host, port), handler_class)
     File "/usr/lib/python2.7/SocketServer.py", line 419, in __init__
       self.server_bind()
     File "/usr/lib/python2.7/wsgiref/simple_server.py", line 48, in server_bind
       HTTPServer.server_bind(self)
     File "/usr/lib/python2.7/BaseHTTPServer.py", line 108, in server_bind
       SocketServer.TCPServer.server_bind(self)
     File "/usr/lib/python2.7/SocketServer.py", line 430, in server_bind
       self.socket.bind(self.server_address)
     File "/usr/lib/python2.7/socket.py", line 224, in meth
       return getattr(self._sock,name)(*args)
   socket.error: [Errno 98] Address already in use
   >>> import pdb
   >>> pdb.pm()
   > /usr/lib/python2.7/socket.py(224)meth()
   -> return getattr(self._sock,name)(*args)
   (Pdb)


.. rst-class:: dark segue

Everybody Prints
================

.. only:: not slides

   ``print`` is great, if you know what you're looking for

.. rst-class:: dark segue

PDB is Better
=============

.. rst-class:: build white

* PDB lets you explore the state of a running program. Or a dead one.
* PDB will run a program repeatedly as you debug it
* It's extensible, so you can build the tools you need

.. rst-class:: segue dark

PDB 101
=======

.. rst-class:: content-columns-2 snap

Explicit Trace Points
---------------------

.. literalinclude:: /samples/fibonacci_trace.py
   :emphasize-lines: 13

.. rst-class:: column-break-before

::

   $ python samples/fibonacci_trace.py 5
   > /Users/nathan/p/pdb/samples/fibonacci_trace.py(12)<module>()
   -> print (fib(int(sys.argv[-1])))
   (Pdb)

PDB stops before the first statement in your program is executed,
waiting for a command.

.. rst-class:: content-columns-2 snap

``next``
--------

.. literalinclude:: /samples/fibonacci_trace.py
   :emphasize-lines: 14

.. rst-class:: columns-break-before

::

   $ python samples/fibonacci_trace.py 5
   > /Users/nathan/p/pdb/samples/fibonacci_trace.py(14)<module>()
   -> print (fib(sys.argv[-1]))
   (Pdb) next
   ValueError: "invalid literal for int() with base 10: 'samples/fibonacci_trace.py'"
   > /Users/nathan/p/pdb/samples/fibonacci_trace.py(14)<module>()
   -> print (fib(sys.argv[-1]))
   (Pdb)

* ``next`` will execute the next statement (including any calls it
  makes)


.. rst-class:: content-columns-2 snap

``step``
--------

.. literalinclude:: /samples/fibonacci_trace.py
   :emphasize-lines: 3

.. rst-class:: columns-break-before

::

   $ python samples/fibonacci_trace.py 5
   > /Users/nathan/p/pdb/samples/fibonacci_trace.py(14)<module>()
   -> print (fib(sys.argv[-1]))
   (Pdb) step
   --Call--
   > /Users/nathan/p/pdb/samples/fibonacci_trace.py(3)fib()
   -> def fib(n):
   (Pdb)

* ``step`` will stop at the next statement (which may be inside a
  function call)


.. rst-class:: content-columns-2 snap


``cont``
--------

.. literalinclude:: /samples/fibonacci_trace.py

.. rst-class:: columns-break-before

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

* ``cont`` will *continue* execution

.. rst-class:: segue dark

Executing Code Under PDB
========================

pdb.run
-------

* PDB will stop *before* executing the first statement

::

   >>> pdb.run("fib('25')")
   > <string>(1)<module>()
   (Pdb)

::

   >>> pdb.runcall(fib, 25)
   > /Users/nathan/p/pdb/samples/fibonacci.py(7)fib()
   -> if n <= 1:
   (Pdb)

Running PDB as a Script
-----------------------

::

   $ python -m pdb samples/fibonacci.py 5
   > /Users/nathan/p/pdb/samples/fibonacci.py(1)<module>()
   -> import sys
   (Pdb)


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

Debugging with PDB
==================

Our Buggy Program
-----------------

Consider a small web application that provides a `postfix notation`_
calculator. You pass your arguments as path elements, and it applies
them to the stack and returns the result.

::

   $ curl http://localhost:8000/2/1/+
   The answer is 3
   $ curl http://localhost:8000/2/10/\*
   The answer is 20
   curl http://localhost:8000/2/10/+/2/\*
   The answer is 24

.. nextslide::

It's cool, but not great with unexpected input.

::

   $ curl http://localhost:8000/2/abc/+/
   Traceback (most recent call last):
     ...
     File "/Users/nathan/p/pdb/samples/pfcalc_wsgi.py", line 39, in handle
       handler.run(self.server.get_app())
     File "/Users/nathan/p/pdb/samples/pfcalc_wsgi.py", line 17, in run
       self.result = application(self.environ, self.start_response)
     File "pfcalc.py", line 46, in rpn_app
       c.push(element)
     File "pfcalc.py", line 28, in push
       value = int(value_or_operator)
   ValueError: invalid literal for int() with base 10: 'abc'

.. nextslide::

We can run it under ``pdb`` to see what's actually happening when it
blows up.

::

   python -m pdb pfcalc.py
   > /Users/nathan/p/pdb/samples/pfcalc.py(1)<module>()
   -> from wsgiref.simple_server import make_server
   (Pdb) cont
   Serving on port 8000...

::

   $ curl http://localhost:8000/2/abc/+

.. nextslide::

Now when we hit the bad URL with ``curl``, Python drops into PDB.

::

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
   Uncaught exception. Entering post mortem debugging
   Running 'cont' or 'step' will restart the program
   > /Users/nathan/p/pdb/samples/pfcalc.py(28)push()
   -> value = int(value_or_operator)
   (Pdb)


Inspecting State
----------------

You can ``p``\ rint the value of a variable.

::

   > /Users/nathan/p/pdb/samples/pfcalc.py(28)push()
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

You can also give it additional parameters to control what lines are shown.

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

.. nextslide::
   :classes: tip content-columns-2 content-smaller

.. rst-class:: span-columns

Python 3.2 added the long list (``ll``) command, which lets you see
the entire function.

.. code-block:: none

   (Pdb) list
    22  	            value = self.OPERATORS[value_or_operator](
    23  	                self.state.pop(),
    24  	                self.state.pop(),
    25  	            )
    26  	        else:
    27  ->	            value = int(value_or_operator)
    28
    29  	        self.state.append(value)
    30
    31  	    def result(self):
    32

.. code-block:: none

   (Pdb) ll
    19  	    def push(self, value_or_operator):
    20
    21  	        if value_or_operator in self.OPERATORS:
    22  	            value = self.OPERATORS[value_or_operator](
    23  	                self.state.pop(),
    24  	                self.state.pop(),
    25  	            )
    26  	        else:
    27  ->	            value = int(value_or_operator)
    28
    29  	        self.state.append(value)


Pretty Print
------------

You can pretty print the value of a variable using the ``pp`` command.

::

   (Pdb) pp self.state
   [2]
   (Pdb) pp self.OPERATORS
   {'*': <slot wrapper '__mul__' of 'int' objects>,
    '+': <slot wrapper '__add__' of 'int' objects>,
    '/': <slot wrapper '__div__' of 'int' objects>}
   (Pdb)


Evaluating Expressions
----------------------

You can also evaluate expressions using the ``!`` command.

::

   (Pdb) !int(value_or_operator)
   *** ValueError: invalid literal for int() with base 10: 'abc'
   (Pdb) !len(self.state)
   1


.. admonition:: ``interact``

   New in Python 3.2, the ``interact`` command gives you an
   interactive prompt with the same locals and globals as the current
   position. This makes it easier to evaluate expressions and explore
   the current position in the code.

   ::

      (Pdb) interact
      *interactive*
      >>> locals().keys()
      dict_keys(['make_server', 'self', 'httpd', '__name__', '__builtins__', 'CalculatorWSGIHandler', '__file__', 'value_or_operator', 'CalculatorServer', 'Calculator', 'rpn_app'])


.. rst-class:: segue dark

Navigating Execution
====================

.. nextslide::

Let's consider another example where our calculator isn't so hot.

::

   $ curl http://localhost:8000/2/3/+/5
   Traceback (most recent call last):
     ...
     File "/System/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/SocketServer.py", line 649, in __init__
       self.handle()
     File "/Users/nathan/p/pdb/samples/pfcalc_wsgi.py", line 39, in handle
       handler.run(self.server.get_app())
     File "/Users/nathan/p/pdb/samples/pfcalc_wsgi.py", line 17, in run
       self.result = application(self.environ, self.start_response)
     File "pfcalc.py", line 54, in rpn_app
       "The answer is %d" % (c.result(),),
     File "pfcalc.py", line 36, in result
       raise SyntaxError("Invalid expression.")
   SyntaxError: Invalid expression.
   > /Users/nathan/p/pdb/samples/pfcalc.py(36)result()
   -> raise SyntaxError("Invalid expression.")
   (Pdb)


.. rst-class:: content-smaller

Where am I?
-----------

The ``where`` command shows the call stack that got us into this mess.

::

   (Pdb) where
     /System/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/pdb.py(1314)main()
   -> pdb._runscript(mainpyfile)
     /System/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/pdb.py(1233)_runscript()
   -> self.run(statement)
     /System/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/bdb.py(400)run()
   -> exec cmd in globals, locals
     <string>(1)<module>()
     /Users/nathan/p/pdb/samples/pfcalc.py(1)<module>()
   -> from wsgiref.simple_server import make_server
     /System/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/SocketServer.py(238)serve_forever()
   -> self._handle_request_noblock()
     /System/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/SocketServer.py(297)_handle_request_noblock()
   -> self.handle_error(request, client_address)
     /System/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/SocketServer.py(295)_handle_request_noblock()
   -> self.process_request(request, client_address)
     /System/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/SocketServer.py(321)process_request()
   -> self.finish_request(request, client_address)
     /System/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/SocketServer.py(334)finish_request()
   -> self.RequestHandlerClass(request, client_address, self)
     /System/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/SocketServer.py(649)__init__()
   -> self.handle()
     /Users/nathan/p/pdb/samples/pfcalc_wsgi.py(39)handle()
   -> handler.run(self.server.get_app())
     /Users/nathan/p/pdb/samples/pfcalc_wsgi.py(17)run()
   -> self.result = application(self.environ, self.start_response)
     /Users/nathan/p/pdb/samples/pfcalc.py(54)rpn_app()
   -> "The answer is %d" % (c.result(),),
   > /Users/nathan/p/pdb/samples/pfcalc.py(36)result()
   -> raise SyntaxError("Invalid expression.")
   (Pdb)

Navigating the Stack
--------------------

You can use the ``up`` command to move one frame up the stack.

::

   (Pdb) up
   > /Users/nathan/p/pdb/samples/pfcalc.py(54)rpn_app()
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
    58  	httpd = make_server('', 8000, rpn_app,
    59  	                    server_class=CalculatorServer,
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

Our server starts with the following lines:

.. code-block:: python

   httpd = make_server('', 8000, rpn_app,
                       server_class=CalculatorServer,
                       handler_class=CalculatorWSGIHandler,
   )
   print "Serving on port 8000..."
   httpd.serve_forever()

.. nextslide::

Using post-mortem debugging is the same as modifying that to something
like:

.. code-block:: python

   try:
     httpd = make_server('', 8000, rpn_app,
                         server_class=CalculatorServer,
                         handler_class=CalculatorWSGIHandler,
     )
     print "Serving on port 8000..."
     httpd.serve_forever()
   except:
     import pdb
     pdb.post_mortem()  # debug the exception being handled

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
   > /home/nathan/p/pdb/samples/pf_settrace.py(15)<module>()->None
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

.. only:: not slides

   We can do this with a breakpoint.

.. code-block:: bash
   :emphasize-lines: 4

   $ python -m pdb pfcalc.py
   > /home/nathan/p/pdb/samples/pfcalc.py(1)<module>()
   -> from wsgiref.simple_server import make_server
   (Pdb) break pfcalc.rpn_app
   Breakpoint 1 at /home/nathan/p/pdb/samples/pfcalc.py:41
   (Pdb) cont
   Serving on port 8000...

.. rst-class:: content-columns-2

Setting Breakpoints
-------------------

.. literalinclude:: /samples/pfcalc.py
   :pyobject: rpn_app

.. code-block:: bash
   :emphasize-lines: 4

   $ python -m pdb pfcalc.py
   > /home/nathan/p/pdb/samples/pfcalc.py(1)<module>()
   -> from wsgiref.simple_server import make_server
   (Pdb) break pfcalc.py:41
   Breakpoint 1 at /home/nathan/p/pdb/samples/pfcalc.py:41
   (Pdb) cont
   Serving on port 8000...

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

   b(reak) ([file:]lineno | function) [, condition]


.. nextslide::

If we make a request to our application, we'll see it drop into PDB.

::

   $ curl http://localhost:8000/2/3/+

::

   > /home/nathan/p/pdb/samples/pfcalc.py(43)rpn_app()
   -> c = Calculator()
   (Pdb) n
   > /home/nathan/p/pdb/samples/pfcalc.py(45)rpn_app()
   (Pdb) !environ['PATH_INFO']
   '/2/3/+'

.. nextslide::

Issuing the ``break`` command without any arguments will report on the
defined breakpoints::

  (Pdb) break
  Num Type         Disp Enb   Where
  1   breakpoint   keep yes   at /home/nathan/p/pdb/samples/pfcalc.py:41
          breakpoint already hit 1 times
  (Pdb) cont
  127.0.0.1 - - [09/Mar/2014 17:18:42] "GET /2/3/+ HTTP/1.1" 200 15


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
   1   breakpoint   keep yes   at /home/nathan/p/pdb/samples/pfcalc.py:41
           breakpoint already hit 4 times


Toggling Breakpoints
--------------------

The breakpoint number (``1``) above can be used to control its
behavior with the following commands:

* ``disable [bpnum]`` disables the given breakpoint. The breakpoint
  remains set, but will not be triggered when the line is encountered.
* ``enable [bpnum]`` enables the given breakpoint.
* ``ignore bpnum [count]`` will ignore a breakpoint for [count] hits.
* ``clear [bpnum]`` clears the breakpoints specified. If no breakpoints are
  specified, prompt to clear all breakpoints.

.. rst-class:: content-flexbox content-vcenter content-big-example

Breakpoint Conditions
---------------------

.. only:: not slides

   You may have noticed that the ``break`` command has this optional
   ``condition`` parameter at the end.

::

   b(reak) ([file:]lineno | function) [, condition]

.. only:: not slides

   You can also specify a condition for a breakpoint. When the breakpoint
   is encountered, the condition is evaluated. If it evaluates True, you
   enter the debugger. A condition can be specified as the final argument
   to the ``break`` command. It can also be set (or changed) later with
   the ``condition`` command.

.. nextslide::

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

.. nextslide::

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

.. rst-class:: segue dark

Extending PDB
=============

Aliases
-------

PDB supports defining aliases for actions you take frequently.

::

  alias d pp dir(%1)

::

  alias printdict for key, value in %1.items(): print "%s: %s" % (key, value)
  alias pd printdict

.. only:: not slides

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
.. _`postfix notation`: http://en.wikipedia.org/wiki/Postfix_notation
