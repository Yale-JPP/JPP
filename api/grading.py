# from sys import exit, stderr
import os.path
# import argparse
from settings import BASE_GRADE
from preprocessing import preliminary_pronunciation_check
from analysis import grade_pitch_pattern

def calculate_grade(sf, sf_array, word, word_array, accent_type):
    """Grade the input sound clip given 5 arguments:
    Takes in the sound clip (sf), the full word (word), and the
    pitch accent pattern type.
    Also expects to be passed in a set of parallel arrays that has the sound clips and words broken
    down into its individual mora.
    Returns a number value between 0 and 100 representing accuracy of pronunciation."""
    grade = 0
    coefficient = preliminary_pronunciation_check(sf, word)
    print(f"Coefficient = {coefficient}")

    if coefficient != 0: # if it is worth it to grade the sound file
        # start with a base value that will be weighted according to the coefficient found.
        grade += BASE_GRADE
        grade += (100 - BASE_GRADE) * grade_pitch_pattern(soundfiles=sf_array, accent_type=accent_type, word=word_array)

    return coefficient * grade

# intended to be used in the command line while in development.
# def init_parser():
#     parser = argparse.ArgumentParser(allow_abbrev=False,
#                                      description='sound analysis')
#     parser.add_argument('filename', nargs='?', help='the filename of the soundfile to analyze', type=str)
#     parser.add_argument('accent_type', nargs='?', help='accent type of the word being said. one of 0, 1, 2, 3, or 4', type=int)
#     parser.add_argument('expected_text', nargs='?', help='the word being said in the soundfile', type=str)
#     return parser

# def main():
#     # current CLI interface lets us test individual sound files as well as the hard-coded example
#     # parser = init_parser()
#     # args = parser.parse_args()
#     # filename = args.filename
#     # accent_type = args.accent_type
#     # expected_text = args.expected_text

#     full_soundclip = ""
#     soundfile_array = []
#     accent_type = 0
#     expected_text = ""


#     if full_soundclip is None or expected_text is None:
#         print("Incorrect parameters")
#         return

#     print(f"Currently reading: {full_soundclip}")
#     if not os.path.isfile(full_soundclip):
#         print("File not found")
#         return

#     for soundfile in soundfile_array:
#         if not os.path.isfile(soundfile):
#             print("File not found")
#             return

#     grade = 0
#     coefficient = preliminary_pronunciation_check(full_soundclip, expected_text)
#     # coefficient = 1 # for testing purposes to bypass coeff calculations
#     print(f"Coefficient = {coefficient}")
#     if coefficient != 0: # if it is worth it to grade the sound file
#         # start with a base value that will be weighted according to the coefficient found.
#         grade += BASE_GRADE
#         grade += (100 - BASE_GRADE) * grade_pitch_pattern(soundfiles=soundfile_array, accent_type=accent_type, word=expected_text)

#     return coefficient * grade

# if __name__ == "__main__":
#     main()