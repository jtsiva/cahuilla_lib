#!/usr/bin/python3

import argparse
import json

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='')

    parser.add_argument('string', type=str,
                    help='String to rewrite in various orthographies')

    args = parser.parse_args()
    convert_dict = []
    with open('../sounds/orthography.json', 'r') as f:
        convert_dict = json.load(f)

    #print (convert_dict)

    for key in convert_dict:
        convert_dict[key]['conv'] = ''
        for ch in args.string:
            if ch is not '':
                pass
            