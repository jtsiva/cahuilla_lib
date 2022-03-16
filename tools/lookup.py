#!/bin/python3
from dictionary.dictionary import Dictionary
import argparse

def main():
    cah_dict = Dictionary("dictionary/schema_v2.json", "../words/dict.json")

if __name__ == "__main__":
    main()