GoodHex, a Good (enough) Hex Editor
===================================

by Travis Goodspeed

This is a quick attempt at a hex editor in python, mostly because I'm
too lazy to learn the internals of Emacs' hexl-mode.  I'm more
interested in annotations and overlays than in gigantic filesizes, and
I don't expect this to be of use to anyone else.



This editor is arranged in a modular fashion around Views, Sources,
and Notes.  At present there is only one view, GHVCurses, which
displays an ncurses view of the present working environment.  I'd
replace this with an X11 viewer, except that I don't give a damn.

Sources are used to provide access to file or device sources.  For
example, you might want to use GHSFileMmap to access an mmap()ed file,
but you'd want something leaner for accessing large disks or disk
images.

Notes are *either* annotations or parsers for different file formats.
The simplest of these is GHNZeroes which does little more than
highlight zeroes while navigating a file.  Future parsers might
include a PNG parser for working with PNG files, or a PE parser for
working with PE files.  As an inspiration for this project was the
Corkami project, support for multiple, conflicting parsers will be
built-in.

For interactive note taking, annotations allow the user to mark bytes
and ranges with color coding and text notes.  For example, a user
might want to mark particular ranges that disagree with the parsers.
These are stored in a SQLite database, for ease of parsing by other
file formats.



Urgent TODO
===========

The following things are needed before any sort of public release.

(1) Proper command-line argument parsing.
(2) Parsers for a few file formats.  (Not shotgun!)
(3) Page up, Page down.
(4) ^D to exit.
(5) Corkami examples


Key Commands
============

Keys are arranged in a series of modes, somewhat like vi but written
by an emacs user.  The default mode is Command Mode, which can always
be reached by pressing ESC twice.

All Modes:
Arrows  -- Move by one or sixteen bytes.
ESC ESC -- Back to Command Mode
TAB     -- Advance to the next set of Notes.

Command Mode:
n/p     -- Move by 0x0100 bytes.
N/P     -- Move by 0x1000 bytes.
q       -- Quit.
i       -- Insert Mode
a       -- Annotation Mode
A       -- ASCII Mode

ASCII Mode:
letters -- Characters go in directly, but not control codes.
	   Newlines are Unix-style.

Insert Mode:
0-9a-F  -- Overwrite bytes.
A       -- ASCII mode.

Annotate Mode:
0-9     -- Colors the given byte.
s       -- Annotates the byte with a known structure.
n       -- Adds a text note to the byte.


