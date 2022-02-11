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

    args = parser.parse_args()

    output = []






if __name__ == "__main__":
    main()