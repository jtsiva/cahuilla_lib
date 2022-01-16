#!/usr/bin/python3

import argparse
import json

def get_orthography(string, ortho_dict):
    """
    Check string
    """
    matching_ortho = "None"
    # sort characters in orthography by length and then match
    # the orthography that matches all the characters in the
    # fewest matches (matching more multi character sounds)
    # is the correct one

    best_match_score = len(string) + 1 #anything should be less than this
    for ortho_name in ortho_dict:
        test_str = string
        match_score = 0
        # print (ortho_name)
        for char in sorted(ortho_dict[ortho_name], key=len, reverse=True):
            # print (f"{char} -> {test_str}")
            match_score += test_str.count(char) #how many occurrences
            test_str = test_str.replace(char, "") #remove matches
            

        if 0 == len(test_str) and match_score < best_match_score:
            matching_ortho = ortho_name
            best_match_score = match_score

    return matching_ortho


def convert_orthography(text, ortho_dict):
    orthography = get_orthography(text, ortho_dict)
    output = ""
    
    # print (orthography)
    for key in ortho_dict:
        new_str = text
        if len(ortho_dict[orthography]) == len(ortho_dict[key]):
            for i in range(len(ortho_dict[orthography])):
                new_str = new_str.replace(ortho_dict[orthography][i], ortho_dict[key][i])

            output += f"{key}: {new_str}\n"

    return output.strip()

def main():
    parser = argparse.ArgumentParser(description='')

    parser.add_argument('string', type=str,
                    help='String to rewrite in various orthographies')

    args = parser.parse_args()

    with open('../sounds/orthography.json') as file:
        ortho_dict = json.load(file)

    # print (get_unique_chars(ortho_dict))

    # print (get_orthography(args.string, get_unique_chars(ortho_dict)))

    print(convert_orthography(args.string, ortho_dict))
    
            
if __name__ == "__main__":
    main()