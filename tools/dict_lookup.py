#!/bin/python3
from dictionary.dictionary import Dictionary
import argparse

def main():
    parser = argparse.ArgumentParser(description='look up entries in the dictionary based on the default Whoosh query langauge')

    parser.add_argument('search_term', type=str,
                    help='Search term to use for searching the dictionary')

    args = parser.parse_args()

    cah_dict = Dictionary("dictionary/schema_v2.json", "../words/dict.json")

    cah_dict.load()

    results = cah_dict.lookup(args.search_term)
    if 0 == len(results):
        print ("No results!")
    else:
        for hit in results:
            print("- {}\n".format(hit))

        print ('top result: {}'.format(cah_dict.get(results[0]['id'])) )

if __name__ == "__main__":
    main()