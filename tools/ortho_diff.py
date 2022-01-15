#!/usr/bin/python3

import argparse
import json

def get_unique_chars(ortho_dict):
    """
    Return the characters that are unique to each orthogrophy
    """
    unique_ortho_chars = {}
    for key in ortho_dict:
        # print (len(ortho_dict[key]))
        unique_ortho_chars[key] = set(ortho_dict[key])
        for key2 in ortho_dict:
            if key != key2:
                # unique_ortho_chars[key].difference_update (set(ortho_dict[key2]))
                unique_ortho_chars[key] =  set(ortho_dict[key]) - (set(ortho_dict[key2]))


    print (unique_ortho_chars)

    return unique_ortho_chars

def get_orthography(string, ortho_dict):
    """
    Check string
    """
    matching_ortho = "None"
    # for key, chars in unique_ortho_chars.items():
    #     if any(char in string for char in chars):
    #         matching_ortho = key

    keys_to_check = []

    #check for characters that don't exist in orthography
    for key, chars in get_unique_chars(ortho_dict).items():
        if any(char in string for char in chars):
            keys_to_check.append(key)

    #Now check
    for key in keys_to_check:
        test_str = string
        print (key)
        for char in ortho_dict[key]:
            print (f"{char} -> {test_str}")
            test_str = test_str.replace(char, "")
            

        if 0 == len(test_str):
            matching_ortho = key
            break

    return matching_ortho


def convert_orthography(text, ortho_dict):
    orthography = get_orthography(text, ortho_dict)
    output = ""
    
    print (orthography)
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