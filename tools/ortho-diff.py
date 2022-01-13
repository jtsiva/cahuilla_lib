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

def get_orthography(str, unique_ortho_chars):
    """
    Check string
    """
    for key, chars in unique_ortho_chars:
        if 

def main():
    parser = argparse.ArgumentParser(description='')

    parser.add_argument('string', type=str,
                    help='String to rewrite in various orthographies')

    args = parser.parse_args()

    with open('../sounds/orthography.json', 'r') as file:
        ortho_dict = json.load(file)

    print (get_unique_chars(ortho_dict))

    #print (ortho_dict)

    # for key in ortho_dict:
    #     ortho_dict[key]['conv'] = ''
    #     for ch in args.string:
    #         if ch is not '':
    #             pass
            
if __name__ == "__main__":
    main()