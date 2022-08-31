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

    
        
        # print (orthography)
        for target_orthography in self.orthography_dict:
            conversion_table = {}
            if len(self.orthography_dict[src_orthography]) == len(self.orthography_dict[target_orthography]):
                for char in sorted(self.orthography_dict[src_orthography], key=len, reverse=True):
                    
                    char_index = self.orthography_dict[src_orthography].index(char)
                    conversion_table[char] = self.orthography_dict[target_orthography][char_index]
                    # if "'" == char:
                    #     print (conversion_table[char])
                    
            # new_str = text
            # remaining_chars = text
            # if len(self.orthography_dict[orthography]) == len(self.orthography_dict[key]):
                # convert = create_convert(self.orthography_dict[orthography], self.orthography_dict[key], text)

                # new_str = convert(0,len(text), 0)

                # print (replace (sorted(self.orthography_dict[orthography], key=len, reverse=True), self.orthography_dict[orthography], self.orthography_dict[key], text
                # ))
                # for char in sorted(self.orthography_dict[orthography], key=len, reverse=True):
                #     char_index = self.orthography_dict[orthography].index(char)
                #     if "'" == char:
                #         print (char_index)
                #     if new_str.find(self.orthography_dict[orthography][char_index]) and remaining_chars.find(self.orthography_dict[orthography][char_index]):
                #         new_str = new_str.replace(self.orthography_dict[orthography][char_index], self.orthography_dict[key][char_index])
                #         if "'" == char:
                #             print (char_index)
                #         if 38 == char_index:
                #             print(self.orthography_dict[key][char_index])
                #         print(new_str)
                #         print(remaining_chars)
                #         remaining_chars = remaining_chars.replace(self.orthography_dict[orthography][char_index], "")

                    # marker_str = marker_str.replace(self.orthography_dict[orthography][char_index], "")
                #     if "í" in char or 'i' in char:
                #         print (char_index)
                #         print(new_str)

                output["converted"][target_orthography] = custom_make_translation(text, conversion_table)#text.translate(str.maketrans(conversion_table))
                
        return output

def custom_make_translation(text, translation):
    regex = re.compile('|'.join(map(re.escape, translation)))
    return regex.sub(lambda match: translation[match.group(0)], text)


def create_convert(src_chars, dest_chars, text):
    sorted_src = sorted(src_chars, key=len, reverse=True)
    def convert (start, end, i):
        if i >= len(src_chars) or start > end:
            return ""
        char_index = src_chars.index(sorted_src[i])
        index = text[start:end].find(sorted_src[i])
        if -1 == index:
            return convert(start, end, i+1)
        else:
            new_char = dest_chars[char_index]
            return convert(start, index, i+1) + new_char + convert(index + 1, end, i);

    return convert



def replace(search_chars, src_chars, dest_chars, word):
    char_index = src_chars.index(search_chars[0])

    remainder = word.replace(src_chars[char_index], "")
    if len(word) > len(remainder):
        return dest_chars[char_index]
    else:
        return word.replace(src_chars[char_index], replace(search_chars[1:], src_chars, dest_chars, remainder))