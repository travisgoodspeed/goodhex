#!/usr/bin/env python3.4
#
# An attempt at a custom hex editor.
# by Travis Goodspeed

from GHView import *;
from GHSource import *;
from GHNotes import *;
from curses import wrapper;
import sys;


def usage():
    print(
"""GoodHex is a nifty little hex editor from Travis Goodspeed, but
it's pretty damned awkward to use without reading the documentation.
In particular, that rotten scoundrel uses words in weird ways and
assumes that users will mess with the source code.

usage:
goodhex file.bin

"""
);
def main(screen):
    """Main method, until I get around to abstracting the gui."""
    view=GHVCurses(screen,source,notes);
    view.mainloop();

if len(sys.argv)<2:
    #source=GHSZeroes();
    usage();
    sys.exit(1);
else:
    #source=GHSFileMmap(sys.argv[1]);
    source=GHSFile(sys.argv[1]);
    #source=GHSFileIhex(sys.argv[1]);

#if len(sys.argv)<3:
#    notes=[GHNZeroes(source),GHNSqlite(source)];
#else:
#    notes=[GHNZeroes(source),GHNPng(source)];

notes=[GHNSqlite(source),GHNZeroes(source)];
wrapper(main);

