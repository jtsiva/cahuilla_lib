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
        if 'cahuilla' in new_entry and len(new_entry['cahuilla']) > 0:
            results = cah_dict.lookup("cahuilla:" + new_entry['cahuilla'])

            #there is a perfect match
            if len(results) == 1:
                print("Entry already exists!\n*{}".format(results[0]))
            else:
                print ("Adding...")
                result = cah_dict.add(new_entry)
                if result:
                    print ("Added: {}".format(new_entry))
                    #save
                    cah_dict.save()
                else:
                    print ("Failed. Check that data conforms to schema.")
        #add
    elif 'rm' in args.command:
        id_to_delete = args.argument
        entry = cah_dict.get(id_to_delete)

        ans = input ("{}\nAre you sure you want to delete this entry?  (y/n)".format(entry))
        if 'y' in ans:
            cah_dict.delete(id_to_delete)
            print("Deleted!")
            #save
            cah_dict.save()
        else:
            print("Aborted")
    else:
        return


    

if __name__ == "__main__":
    main()