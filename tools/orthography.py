#!/bin/python3

import json

class Orthography():
    def __init__ (self, orthography_file):
        self.orthography_dict = {}
        with open(orthography_file) as file:
            self.orthography_dict = json.load(file)

    def get_orthography(self,string):
        """
        Check string
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
        orthography = self.get_orthography(text)
        output = {"source" : orthography, "converted" : {}}

        
        # print (orthography)
        for key in self.orthography_dict:
            new_str = text
            if len(self.orthography_dict[orthography]) == len(self.orthography_dict[key]):
                for i in range(len(self.orthography_dict[orthography])):
                    new_str = new_str.replace(self.orthography_dict[orthography][i], self.orthography_dict[key][i])

                output["converted"][key] = new_str
                
        return output