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

        entry - the starting dictionary--could be a schema
        editable - the status True/False of whether entry is editable
        """
        self._entry = entry
        self.editable = bool(editable)

    def __getitem__ (self, key):
        """
        Return item from _entry.
        key - key from which to get value
        """
        return self._entry[key]

    def __setitem__ (self, key, value):
        """
        Set an item if the entry is set to editable and the key already exists. Raises KeyError if conditions not met

        key - the key to update
        value - the new value for the key
        """

        if self.editable and key in self._entry:
            self._entry[key] = value
        else:
            raise KeyError("Key is not editable or doesn't exist")