#!/bin/python3

import json
import re

class Orthography():
    """
    Pulls in orthographic equivalencies from json, detects
    the input orthography, and outputs alternatives
    """
    def __init__ (self, orthography_file):
        self.orthography_dict = {}
        with open(orthography_file) as file:
            self.orthography_dict = json.load(file)

    def get_orthography(self,string):
        """
        Check string to see which orthography matches
        """
        matching_ortho = "None"
        # sort characters in orthography by length and then match
        # the orthography that matches all the characters in the
        # fewest matches (matching more multi character sounds)
        # is the correct one

        best_match_score = len(string) + 1 #anything should be less than this
        for ortho_name in self.orthography_dict:
            test_str = string
            match_score = 0
            # print (ortho_name)
            for char in sorted(self.orthography_dict[ortho_name], key=len, reverse=True):
                # print (f"{char} -> {test_str}")
                match_score += test_str.count(char) #how many occurrences
                test_str = test_str.replace(char, "") #remove matches
                

            if 0 == len(test_str) and match_score < best_match_score:
                matching_ortho = ortho_name
                best_match_score = match_score

        return matching_ortho


    def convert_orthography(self, text):
        """
        Convert from one orthography to another and return
        results
        """
        src_orthography = self.get_orthography(text)
        output = {"source" : src_orthography, "converted" : {}}

        for target_orthography in self.orthography_dict:
            conversion_table = {}

            if len(self.orthography_dict[src_orthography]) == len(self.orthography_dict[target_orthography]):

                for char in sorted(self.orthography_dict[src_orthography], key=len, reverse=True):
                    char_index = self.orthography_dict[src_orthography].index(char)
                    conversion_table[char] = self.orthography_dict[target_orthography][char_index]
                   

                output["converted"][target_orthography] = custom_make_translation(text, conversion_table)
                
        return output

def custom_make_translation(text, translation):
    """
    Alternative to str.translate that allows for multi-char translation
    """
    regex = re.compile('|'.join(map(re.escape, translation)))
    return regex.sub(lambda match: translation[match.group(0)], text)