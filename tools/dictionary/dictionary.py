#!/bin/python3
import os.path
import json
from whoosh.fields import Schema, ID, KEYWORD, TEXT
from whoosh.index import create_in, open_dir
from util.managed_entry import ManagedEntry

class Dictionary():
    def __init__(self, schema_file, word_list_file):
        """
        Load words conforming to schema

        schema_file - file name with json object outlining keys
        word_list_file - file with list of json objects with word data
        """
        self._schema_file = schema_file
        self._entries = []
        self.index = None
        self.schema = None

        with open(schema_file) as file:
            self.schema = json.load(file)

        with open(word_list_file) as file:
            word_list = json.load(file)
            for json_entry in word_list:
                self._entries.append(ManagedEntry(json_entry, False))

    def load (self):
        """
        Load raw word list and create searchable index. If index
        already exists then it is recreated.
        """

        #create Whoosh schema. Based on schema_v2
        self.schema = Schema(cahuilla=ID(stored=True),
                english=KEYWORD(stored=True, commas=True),
                pos=KEYWORD(commas=True),
                origin=ID(),
                related=KEYWORD(commas=True),
                tags=KEYWORD(commas=True),
                source=ID(),
                notes=TEXT(),
                id=ID())

        #create and populate index if it doesn't exist, load otherwise
        if not os.path.exists("index"):
            os.mkdir("index")
            self.index = create_in("index", self.schema)
            writer = self.index.writer()
            for entry in self._entries:
                writer.add_document(cahuilla=entry['cahuilla'],
                english=",".join(entry['english']),
                pos=",".join(entry['pos']),
                origin=entry['origin'],
                related=",".join(entry['related']),
                tags=",".join(entry['tags']),
                source=entry['source'],
                notes="\n".join(entry['notes']),
                id=entry['id'])

            writer.commit()
        else:
            self.index = open_dir("index")

        

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







