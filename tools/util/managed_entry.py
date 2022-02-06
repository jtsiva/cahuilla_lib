#!/bin/python3

class ManagedEntry ():
    """
    Provides a dictionary that can be made readonly and doesn't allow
    additional keys upon creation
    """


    #protected
    _entry = None #python dictionary containing related fields
    

    def __init__ (self, entry, editable):
        """
        Initializer entry data and editable status

        entry - the starting dictionary
        editable - the status True/False of whether entry is editable
        """
        self._entry = entry
        self.editable = bool(editable)

    def __getitem__ (self, key):
        """
        Return item from _entry. Can throw key error
        key - key from which to get value
        """
        return self._entry[key]

    def __setitem__ (self, key, val):

    


