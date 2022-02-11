#!/bin/python3
from ..util.managed_entry import ManagedEntry

class Dictionary():
    def __init__(self, schema_file, word_list):
        """
        Load words conforming to schema

        schema_file - file name with json object outlining keys
        word_list - list of json objects with word data
        """
        self._schema_file = schema_file
        self._entries = []

        for json_entry in word_list:
            self._entries.append(ManagedEntry(json_entry, False))

    





