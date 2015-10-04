#!/usr/bin/env python3
#
# Data sources for my hex editor.  For now, I just support an empty
# file and an mmap()ed file, but later revisions will support
# networked block devices and RAM-cached files.

import mmap;

class GHSZeroes():
    """Null source consisting of an infinite number of zeroes."""
    length=-1;  #Infinite
    def getbyte(self,adr):
        """Gets a byte."""
        return adr&0xFF;
    def setbyte(self,adr,val):
        """Ignores setting the byte."""
        return;

class GHSFileMmap():
    """File source powered by mmap."""
    f=None;
    mm=None;
    length=-1;  #Don't yet support length limits.
    def __init__(self,
                 filename):
        """Opens a file by mmmap() for use within GoodHex."""
        f=open(filename,"r+b");      #Open the file.
        mm=mmap.mmap(f.fileno(),0);  #Map the whole file.
        self.f=f;
        self.mm=mm;
    def getbyte(self,adr):
        """Gets a byte."""
        try:
            return self.mm[adr];
        except:
            return None;
    def setbyte(self,adr,val):
        """Writes a byte."""
        try:
            self.mm[adr]=val;
            return 1;
        except:
            pass;
        return 0;

class GHSFile():
    """File source held in RAM."""
    f=None;
    b=None;
    length=-1;
    def __init__(self,
                 filename):
        """Opens a file by mmmap() for use within GoodHex."""
        f=open(filename,"r+b");      #Open the file.
        b=f.read();
        self.b=b;
        self.length=len(b);
        f.close();
    def getbyte(self,adr):
        """Gets a byte."""
        if adr<len(self.b):
            return self.b[adr];
        else:
            return None;
    def setbyte(self,adr,val):
        """Writes a byte."""
        return 0;

class GHSFileIhex():
    """Sparse file source from Intel Hex held in RAM."""
    f=None;
    b=None;
    length=-1;  #Don't yet support length limits.
    def __init__(self,
                 filename):
        """Opens a file by mmmap() for use within GoodHex."""
        from intelhex import IntelHex;
        self.ihex=IntelHex(filename);
        self.ihex.padding=None;
    def getbyte(self,adr):
        """Gets a byte."""
        return self.ihex[adr];
        
    def setbyte(self,adr,val):
        """Writes a byte."""
        self.ihex[adr]=val;

