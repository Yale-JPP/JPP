from sys import exit, stderr
import os.path
import argparse
from settings import BASE_GRADE
from preprocessing import preliminary_pronunciation_check
from analysis import grade_pitch_pattern

# currently intended to be used in the command line while in development.
# def init_parser():
#     parser = argparse.ArgumentParser(allow_abbrev=False,
#                                      description='sound analysis')
#     parser.add_argument('filename', nargs='?', help='the filename of the soundfile to analyze', type=str)
#     parser.add_argument('accent_type', nargs='?', help='accent type of the word being said. one of 0, 1, 2, 3, or 4', type=int)
#     parser.add_argument('expected_text', nargs='?', help='the word being said in the soundfile', type=str)
#     return parser

def main():
    # current CLI interface lets us test individual sound files as well as the hard-coded example
    # parser = init_parser()
    # args = parser.parse_args()
    # filename = args.filename
    # accent_type = args.accent_type
    # expected_text = args.expected_text

    full_soundclip = ""
    soundfile_array = []
    accent_type = 0
    expected_text = ""


    if full_soundclip is None or expected_text is None:
        print("Incorrect parameters")
        return

    print(f"Currently reading: {full_soundclip}")
    if not os.path.isfile(full_soundclip):
        print("File not found")
        return

    for soundfile in soundfile_array:
        if not os.path.isfile(soundfile):
            print("File not found")
            return

    grade = 0
    coefficient = preliminary_pronunciation_check(full_soundclip, expected_text)
    # coefficient = 1 # for testing purposes to bypass coeff calculations
    print(f"Coefficient = {coefficient}")
    if coefficient != 0: # if it is worth it to grade the sound file
        # start with a base value that will be weighted according to the coefficient found.
        grade += BASE_GRADE
        grade += (100 - BASE_GRADE) * grade_pitch_pattern(soundfiles=soundfile_array, accent_type=accent_type, word=expected_text)

    return coefficient * grade

if __name__ == "__main__":
    main()