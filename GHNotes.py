#!/usr/bin/env python3
#
# These classes provide note and annotation services to the hex
# editor.  The editor allows for multiple annotations of a single
# file, some of which are read-only and some of which are interactive.
#
# For example, Ange's multi-PE from Corkami and POC||GTFO 0x01 might
# be annotated three ways for the three different Windows versions.


class GHNZeroes():
    """Simple dummy class that colors bytes by value."""
    src=None;
    def __init__(self,source):
        """Initializes around the source, which ought to be used
        sparingly if at all."""
        self.src=source;
    def getcolor(self,badr,b,adr):
        """Returns a 1-digit color for the given byte address, byte,
        and cursor address."""
        if b==None or b==0: return 2;
        return 0;
    def setcolor(self,adr,color):
        """Sets the color of a byte."""
        return 0;
    def getname(self):
        """Returns the name of the notation scheme."""
        return "Zero Marker";

    def getnote(self,adr):
        """Returns a note for the given byte."""
        return None;
class GHNSqlite():
    """Annotation class for storing notes in a SQLite3 database.
    Berkeley DB might be a better choice for absurdly large files, but
    this ought to work for now."""
    
    db=None;
    src=None;
    filename=None;
    c=None;
    def __init__(self,source,filename="goodhex.db"):
        self.src=source;
        import sqlite3;
        self.db=sqlite3.connect(filename);
        c=self.db.cursor();
        self.c=c;
        self.filename=filename;
        
        #Now init the database, if it's not already initialized.
        c.execute("create table if not exists colors(adr integer primary key,color)");
        c.execute("create table if not exists notes(adr integer primary key,note)");
        #TODO types, weirder stuff.
    def getcolor(self,badr,b,adr):
        """Returns a 1-digit color code fro the given byte address,
        byte, and cursor address."""
        self.c.execute("select note from notes where adr=?", (badr,));
        try:
            row=self.c.fetchone();
            row[0];
            return 8;
        except:
            pass;
        
        self.c.execute("select color from colors where adr=?", (badr,));
        try:
            row=self.c.fetchone();
            return row[0];
        except:
            return 0;
        
    def setcolor(self,adr,color):
        """Sets the color of the current byte."""
        self.c.execute("delete from colors where adr=?;",
                       (adr,));
        self.c.execute("insert into colors (adr,color) values (?,?);",
                       (adr,color));
        self.db.commit();
    def getname(self):
        """Returns the name of the notation scheme."""
        return self.filename;
    def getnote(self,adr):
        """Returns the note from the given address."""
        self.c.execute("select note from notes where adr=?", (adr,));
        try:
            row=self.c.fetchone();
            return row[0];
        except:
            return None;
    def setnote(self,adr,note):
        self.c.execute("delete from notes where adr=?;",
                       (adr,));
        self.c.execute("insert into notes (adr,note) values (?,?);",
                       (adr,note));
        self.db.commit();
        return;

class GHNPng():
    """Simple parser for PNG files.  For now, it only annotates the
    header.  This really ought to be redone to annotate all the chunks
    as regions, once we have region support."""
    src=None;
    def __init__(self,source):
        """Initializes around the source, which ought to be used
        sparingly if at all."""
        self.src=source;
    pngheader=[0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a];
    pngheadernotes=["0x89, high byte is set to detect 7-bit transfers.",
                    "P, N, G to indicate the file type.",
                    "P, N, G to indicate the file type.",
                    "P, N, G to indicate the file type.",
                    "DOS line ending, to detect dos/unix conversion bugs.",
                    "DOS line ending, to detect dos/unix conversion bugs.",
                    "EOF to end display under DOS with the type command.",
                    "Unix line ending, to detect dos/unix conversion bugs."];
    def getcolor(self,badr,b,adr):
        """Returns a 1-digit color for the given byte address, byte,
        and cursor address."""
        if b==None: return 0;
        
        #For the header, we use color 1 to be good and 2 to be bad.
        if badr<8:
            if self.pngheader[badr]!=b:
                return 1;
            else: return 2;
        
        return 0;
    def getnote(self,adr):
        """Returns a note for the given byte."""
        if adr<8:
            return self.pngheadernotes[adr];
        else:
            return None;
    def setnote(self,adr,note):
        return 0;
    def setcolor(self,adr,color):
        """Sets the color of a byte."""
        return 0;
    def getname(self):
        """Returns the name of the notation scheme."""
        return "PNG Marker";
