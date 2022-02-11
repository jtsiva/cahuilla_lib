#!/bin/python3
import argparse
import json


def main():
    """
    - move existing fields over
    - set new fields
    """

    

    parser = argparse.ArgumentParser(description='convert the word lists from v1 to v2')

    parser.add_argument('input_file', type=str,
                    help='')

    parser.add_argument('output_file', type=str,
                    help='')

    parser.add_argument('start_num', type=int,
                    help='')


    args = parser.parse_args()

    index = args.start_num

    word_list = []
    with open(args.input_file) as file:
        word_list = json.load(file)

    output = []

    for item in word_list:
        entry = {
            "cahuilla": item["cahuilla"],
            "english": item["english"],
            "pos": item["pos"],
            "origin": item['origin'],
            "related" : [],
            "tags": [],
            "source": "",
            "notes": item["notes"],
            "id": "v2_" + str(index)
        }
        index += 1

        if "words_huaute" in args.input_file:
            entry['source'] = "huaute2014havun"
        elif "words_siva-sauvel-chemivillu" in args.input_file:
            entry['source'] = "saubel1981chem"
        elif "words_siva-sauvel-iisniyatam" in args.input_file:
            entry['source'] = "saubel1977iisn"
        elif "words_seiler-dict" in args.input_file:
            entry["source"] = "seiler1979cah"

        output.append(entry)

    with open(args.output_file, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    main()