#!/bin/python3
import json
from collections.abc import MutableMapping

class ManagedEntry (MutableMapping):
    """
    Provides a dictionary that can be made readonly and doesn't allow
    additional keys upon creation
    """

    #protected
    _editable = False
    
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

    def __repr__ (self):
        return str(self._entry)

    def __dict__  (self):
        return self._entry

    def __str__(self):
        return str(self._entry)

    @classmethod
    def from_file(cls, file_name, editable):
        """
        Create object by taking a file name. File should contain a sort of schema with needd keys and default values.

        file_name - name of file from which to load
        editable - whether the object is editable by default
        """
        with open (file_name) as file:
            entry = json.load(file)

        return cls(entry, editable)