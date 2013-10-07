============
In Depth PDB
============

Description (400 Characters)

Python includes a powerful debugger, but using it well requires
practice. Setting a break point and inspecting local variables is
easy, but what else can you do? What if you need to set the breakpoint
in one of your dependencies, or only fire it conditionally? How do you
navigate calls, or change them? Join me for an in depth look at how
you can better use PDB to debug and understand programs.

Audience

Novice programmers surveying the ecosystem, intermediate programmers
looking to level up their understanding of a core Python tool

Objectives

Attendees will get an introduction to using PDB, and an introduction
to advanced usage. Advanced meaning aliases, breakpoint commands, and
pdbrc files.

Abstract

Python's debugger, PDB, is a powerful built-in tool, but its interface
is less than inviting. Many programmers I've worked with use it
simply, if at all: setting a break point, and then inspecting the
local state, occassionally stepping a few lines in, before continuing
or killing the program.

PDB can do so much more.

PDB allows programmers to set breakpoints on the fly, re-run programs
on exit to continue debugging, and inspect and modify execution flow.
And that's just for starters.

By leveraging PDB's features you can fire breakpoints conditionally,
display useful information when they fire, even construct simple
"watches" on variables.

PDB is included in the standard library, which means that there are
additional tools that extend if further, providing ways to debug web
applications and debug over a network connection.

This talk will provide novice Python programmers with a basic
understanding of the Python debugger. Intermediate programmers who
know about PDB will come away with knowledge of how they can better
leverage it when working with their programs.


Outline


* PDB overview (< 5 min)
* Getting into PDB: "-m pdb", set_trace, etc (5 min)
* Inspecting variables and the stack (5 min)
* Navigating execution (5 min)
* Breakpoints: (10 min)
 * Setting and clearing breakpoints in your code and dependencies
 * Conditional breakpoints
 * Executing commands on break
* Creating your own debugger commands (10 min)
* .pdbrc (5 min)
* Q & A

* PDB overview (< 5 min)
* Getting into PDB: "-m pdb", set_trace, etc (5 min)
* Inspecting variables and the stack (5 min)
* Navigating execution
* Breakpoints: (10 min)
** Setting and clearing breakpoints in your code and dependencies
** Conditional breakpoints
** Executing commands on break
* Creating your own debugger commands (5 min)
