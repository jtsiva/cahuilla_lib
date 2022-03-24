#!/bin/python3
import os.path
import json
import sys, logging
from whoosh.fields import Schema, ID, KEYWORD, TEXT
from whoosh.index import create_in, open_dir
from whoosh.qparser import MultifieldParser
from util.managed_entry import ManagedEntry

class Dictionary():
    def __init__(self, schema_file, word_list_file):
        """
        Load words conforming to schema

        schema_file - file name with json object outlining keys
        word_list_file - file with list of json objects with word data
        """
        self._schema_file = schema_file
        self._edited_entries = []
        self.index = None
        self.schema = None
        self.word_list_file = word_list_file

        with open(schema_file) as file:
            self.schema = json.load(file)


    def load (self):
        """
        Load raw word list and create searchable index. If index
        already exists then it is recreated.
        """
        

        #create Whoosh schema. Based on schema_v2
        self.schema = Schema(cahuilla=ID(stored=True),
                english=KEYWORD(stored=True, commas=True),
                pos=KEYWORD(stored=True,commas=True),
                origin=ID(stored=True,),
                related=KEYWORD(stored=True,commas=True),
                tags=KEYWORD(stored=True,commas=True),
                source=ID(stored=True,),
                notes=TEXT(stored=True,),
                id=ID(stored=True))

        #create and populate index if it doesn't exist, load otherwise
        if not os.path.exists("index"):
            logging.debug("Index doesn't exist. Creating...")
            os.mkdir("index")
            self.index = create_in("index", self.schema)
            writer = self.index.writer()
            with open(self.word_list_file) as file:
                word_list = json.load(file)
                for entry in word_list:
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
            logging.debug("Loading index")
            self.index = open_dir("index")

    def _reload (self):
        """
        Delete index and regenerate
        """
        if os.path.exists("index"):
            os.rmdir("index")

        self.load() 

    def lookup(self, search_term):
        """
        Use the search term to return a list of words that best
        match the term. Returns abbreviated entry
        """
        return_words = []

        query_parser = MultifieldParser(["cahuilla", "english", "pos", "origin", "tags", "source", "notes"], schema=self.index.schema)
        query = query_parser.parse(search_term)

        with self.index.searcher() as searcher:
            for hit in searcher.search(query, limit=None):
                return_words.append(hit.fields())


        return return_words

    def get(self, id, editable=False):
        """
        Get a specific ManagedEntry from the dictionary by ID
        """
        result = None

        with open(self.word_list_file) as file:
            word_list = json.load(file)
            for entry in word_list:
                if id in entry.values():
                    result = ManagedEntry(entry, editable)

        return result

    def update (self, updated_entry):
        """
        Provide updated entry to dictionary. Will not replace current
        entry until save() is called

        updated_entry - update version of entry provided by get()
        """
        self._edited_entries.append(updated_entry)

    def save (self):
        """
        Write edited dictionary entries to dictionary json and update
        index
        """
        highest_id = 0
        word_list = None

        #update local copy of dictionary
        with open(self.word_list_file) as file:
            word_list = json.load(file)

            #loop through to find highest id
            
            for entry in word_list:
                if int(entry['id'].split('_')[1]) > highest_id:
                    highest_id = int(entry['id'].split('_')[1])

            highest_id += 1
            logging.debug("Next ID is: %s".format(highest_id))
            #now loop through again to update
            i = 0
            while i < len(word_list):
                entry = word_list[i]
                for updated in self._edited_entries:
                    if updated['id'] in entry.values():
                        updated['id'] = updated['id'].split('_')[0] + highest_id
                        highest_id += 1
                        
                        logging.debug("Updating %s to %s".format(entry, updated))
                        word_list[i] = updated

                i += 1
            #

        #write to file
        json.dump(word_list, self.word_list_file)

        #clear list of pending edits
        self._edited_entries.clear()

        #reload index
        self._reload()

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







