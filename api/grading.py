from sys import exit, stderr
import os.path
import argparse
from settings import BASE_GRADE
from preprocessing import preliminary_pronunciation_check
from analysis import get_sound_info

# currently intended to be used in the command line while in development.
def init_parser():
    parser = argparse.ArgumentParser(allow_abbrev=False,
                                     description='sound analysis')
    parser.add_argument('filename', nargs='?', help='the filename of the soundfile to analyze', type=str)
    parser.add_argument('expected_text', nargs='?', help='the word being said in the soundfile', type=str)
    return parser

def main():
    # current CLI interface lets us test individual sound files as well as the hard-coded example
    parser = init_parser()
    args = parser.parse_args()
    filename = args.filename
    expected_text = args.expected_text

    if filename is None or expected_text is None:
        print("Incorrect parameters")
        return

    print(f"Currently reading: {filename}")
    if not os.path.isfile(filename):
        print("File not found")
        return
    else:
        grade = 0
        coefficient = preliminary_pronunciation_check(filename, expected_text)
        print(f"Coefficient = {coefficient}")
        if coefficient != 0: # if it is worth it to grade the sound file
            # start with a base value that will be weighted according to the coefficient found.
            grade += BASE_GRADE
            get_sound_info(filename, expected_text)

if __name__ == "__main__":
    main()