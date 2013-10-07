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
