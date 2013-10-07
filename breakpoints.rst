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
