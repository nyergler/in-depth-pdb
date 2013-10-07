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
