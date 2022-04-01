import argparse
import sys
import logging
from dictionary.dictionary import Dictionary
import json

def main():
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

    parser = argparse.ArgumentParser(description='Add or remove an entry')

    parser.add_argument('command', type=str,
                    help='add | rm')
    parser.add_argument('argument', type=str,
                    help='argument for given command (json entry or ID')

    args = parser.parse_args()

    cah_dict = Dictionary("dictionary/schema_v2.json", "../words/dict.json")

    cah_dict.load()

    if 'add' in args.command:
        new_entry = json.loads(args.argument)
        #must have a cahuilla word at a minimum
        if 'cahuilla' in new_entry and len(new_entry['cahuilla'] > 0):
            results = cah_dict.lookup("cahuilla:" + new_entry['cahuilla'])

            #there is a perfect match
            if len(results) == 1:
                print("Entry already exists!\n*{}".format(results[0]))
            else:
                print ("Adding...")
                result = cah_dict.add(new_entry)
                if result:
                    print ("Added: {}".format(new_entry))
                else:
                    print ("Failed. Check that data conforms to schema.")
        #add
    elif 'rm' in args.command:
        id_to_delete = args.argument
    else:
        return

    

    # get

    entry = cah_dict.get(args.id, editable=True)

    if type(entry[args.key]) is list:
        entry[args.key] = args.value.split(',')
    else:
        entry[args.key] = args.value

    #update

    cah_dict.update(entry)

    #save
    cah_dict.save()

if __name__ == "__main__":
    main()