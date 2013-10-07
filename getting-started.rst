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
