#!/bin/python3
import os.path
import json
import sys
import logging
import shutil
from whoosh.fields import Schema, ID, KEYWORD, TEXT
from whoosh.index import create_in, open_dir
from whoosh.qparser import MultifieldParser

class Dictionary():
    """
    Dictionary object to manage viewing and editing lists of words with associated data

    TODO: 
        - lookups and edits only operate on committed entries
        - divide save operations between update, add, and delete
    """
    def __init__(self, schema_file, word_list_file):
        """
        Load words conforming to schema

        schema_file - file name with json object outlining keys
        word_list_file - file with list of json objects with word data
        """
        self._schema_file = schema_file
        self._updated_entries = []
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
            shutil.rmtree("index")

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
        Get a specific entry from the dictionary by ID
        """
        result = None

        with open(self.word_list_file) as file:
            word_list = json.load(file)
            for entry in word_list:
                if id in entry.values():
                    result = entry

        return result

    def update (self, updated_entry):
        """
        Provide updated entry to dictionary. Will not replace current
        entry until save() is called

        updated_entry - update version of entry provided by get()
        """
        self._updated_entries.append(("edit", updated_entry))

    def save (self):
        """
        Write edited dictionary entries to dictionary json and update
        index
        """
        word_list = None

        with open(self.word_list_file) as file:
            word_list = json.load(file)

            #check if we need to add entries to the dictionary
            for entry in self._updated_entries:
                if "add" == entry[0]:
                    word_list.append(entry[1])

            to_delete = []
           
            i = 0
            #step through dictionary
            while i < len(word_list):
                entry = word_list[i]
                #loop through update list
                for updated in self._updated_entries:
                    #check if the dictionary entry needs updates
                    if updated[1]['id'] in entry.values():
                        
                        #check if we are editing or deleting the entry
                        if "edit" == updated[0]:
                            logging.debug("Updating {} to {}".format(entry, updated[1]))
                            word_list[i] = updated[1]
                        elif "delete" == updated[0]:
                            #add index to delete list
                            to_delete.append(i)
                #
                i += 1
            #

        #write to file
        with open (self.word_list_file, 'w') as file:
            json.dump(word_list, file, indent=2)

        #clear list of pending edits
        self._updated_entries.clear()

        #reload index
        self._reload()

    def add(self, entry_data):
        """
        Add a word to the dictionary. All data expected by schema
        should be provided
        """

        #loop through to find highest id
        highest_id = 0
        word_list = None

        #findest highest id so that we know our new id
        with open(self.word_list_file) as file:
            word_list = json.load(file)
            for entry in word_list:
                if int(entry['id'].split('_')[1]) > highest_id:
                    highest_id = int(entry['id'].split('_')[1])

        highest_id += 1
        logging.debug("Next ID is: {}".format(highest_id))

        
        #get dictionary entry template
        with open(self._schema_file) as file:
            new_entry = json.load(file)

        #make sure that the new data doesn't unexpected keys
        for key in entry_data:
            if key in new_entry:
                new_entry[key] = entry_data[key]
            else:
                return False


        new_entry['id'] = highest_id
        logging.debug("Adding new entry: {}".format(new_entry))
        highest_id += 1
        self._updated_entries.append(("add", new_entry))

        return True

    def delete(self, entry_id):
        """
        Remove an entry by ID. Takes effect on save
        """
        logging.debug("Deleting: {}".format(entry_id))
        self._updated_entries.append(("delete", {'id':entry_id}))

    def get_usage (self, word):
        """
        Return a list of examples where the word is used
        """
        pass






