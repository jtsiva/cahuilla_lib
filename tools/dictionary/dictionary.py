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

    def lookup(self, search_term):
        """
        Use the search term to return a list of words that best
        match the term
        """
        return_words = None

        return return_words

    def edit (self, field, value):
        """
        Flag or suggest edit
        """
        pass

    def get_usage (self, word):
        """
        Return a list of examples where the word is used
        """
        pass

    def add(self, entry_data):
        """
        Add a word to the dictionary. All data expected by schema
        should be provided
        """
        pass

    def delete(self, entry_id):
        """
        Remove an entry by ID
        """
        pass







