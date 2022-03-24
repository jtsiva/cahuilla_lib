import argparse
import sys
import logging
from dictionary.dictionary import Dictionary

def main():
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
    parser = argparse.ArgumentParser(description='Edit the field of a particular entry')

    parser.add_argument('id', type=str,
                    help='id of entry to update')
    parser.add_argument('key', type=str,
                    help='key to update')
    parser.add_argument('value', type=str,
                    help='new value for key')

    args = parser.parse_args()

    cah_dict = Dictionary("dictionary/schema_v2.json", "../words/dict.json")

    cah_dict.load()

    # get

    entry = cah_dict.get(args.id)

    entry[args.key] = args.value

    #update

    cah_dict.update(entry)

    #save
    cah_dict.save()

if __name__ == "__main__":
    main()