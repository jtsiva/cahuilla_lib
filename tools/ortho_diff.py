#!/usr/bin/python3

import argparse
import json

def get_unique_chars(ortho_dict):
    """
    Return the characters that are unique to each orthogrophy
    """
    unique_ortho_chars = {}
    for key in ortho_dict:
        unique_ortho_chars[key] = set(ortho_dict[key])
        for key2 in ortho_dict:
            if key != key2:
                unique_ortho_chars[key].difference_update (set(ortho_dict[key2]))

    return unique_ortho_chars

def get_orthography(string, unique_ortho_chars):
    """
    Check string
    """
    matching_ortho = "None"
    for key, chars in unique_ortho_chars.items():
        if any(char in string for char in chars):
            matching_ortho = key

    return matching_ortho


def convert_orthography(text, ortho_dict):
    orthography = get_orthography(text, get_unique_chars(ortho_dict))
    output = ""
    new_str = text
    for key in ortho_dict:
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