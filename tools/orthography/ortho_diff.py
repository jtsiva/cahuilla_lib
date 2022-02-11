#!/usr/bin/python3

import argparse
import orthography



def main():
    parser = argparse.ArgumentParser(description='')

    parser.add_argument('string', type=str,
                    help='String to rewrite in various orthographies')

    args = parser.parse_args()

    ortho = orthography.Orthography('../../sounds/orthography.json')



    print(ortho.convert_orthography(args.string))
    
            
if __name__ == "__main__":
    main()