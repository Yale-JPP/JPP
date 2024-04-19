import pykakasi
import numpy as np
import matplotlib.pyplot as plt
from difflib import SequenceMatcher
from settings import HIRAGANA_NOT_FOUND_PENALTY

vowels = ['あ', 'い', 'う', 'え', 'お', 'ん']
skip = ['ゃ', 'ゅ', 'ょ']
data = [
    ("午前", "ごぜんです", 5),
    ("旅館", "りょかんです", 5),
    ("日本", "にほんです", 5),
    ("旅行", "りょこうです", 5),
    ("値段", "ねだんです", 5),
    ("家族", "かぞくです", 5),
    ("社長", "しゃちょうです", 5),
    ("自由", "じゆうです", 5),
    ("試合", "しあいです", 5),
    ("故障", "こしょうです", 5),
    ("予定", "よていです", 5),
    ("地震", "じしんです", 5),
    ("砂糖", "さとうです", 5),
    ("美術", "びじゅつです", 5),
    ("地獄", "じごくです", 5),
    ("都会", "とかいです", 5),
    ("去年", "きょねんです", 5),
    ("二本", "にほんです", 5),
    ("野球", "やきゅうです", 5),
    ("気温", "きおんです", 5),
    ("自分", "じぶんです", 5),
    ("書道", "しょどうです", 5),
    ("予習", "よしゅうです", 5),
    ("佐藤", "さとうです", 5),
    ("気分", "きぶんです", 5),
    ("世界", "せかいです", 5),
    ("仕事", "しごとです", 5),
    ("予報", "よほうです", 5),
    ("試験", "しけんです", 5),
    ("家賃", "やちんです", 5),
    ("時間", "じかんです", 5),
    ("写真", "しゃしんです", 5),
    ("野菜", "やさいです", 5),
    ("胡椒", "こしょうです", 5),
    ("授業", "じゅぎょうです", 5)
]

def plot(pitches):
    """Given a set of pitches, plot them equally spaced in time to see a visualization of the pitch over time."""
    time_axis = np.arange(len(pitches))
    plt.scatter(time_axis, pitches)

    plt.ylabel("Pitch")
    plt.title("Pitch vs. Time")

    plt.show()

def get_kanji_info(input_text):
    kks = pykakasi.kakasi()
    result = kks.convert(input_text)
    return result

def text_to_hiragana(input_text):
    """Given a set of Japanese hiragana, katakana, and kanji, returns the string in all hiragana characters."""
    info = get_kanji_info(input_text)
    hiragana_string = ""
    for word in info:
        hiragana_string += word['hira']
    return hiragana_string

def text_to_romaji(input_text):
    """Given a set of Japanese hiragana, katakana, and kanji, returns the string in all romaji characters."""
    info = get_kanji_info(input_text)
    romaji_string = ""
    for word in info:
        romaji_string += word['hepburn']
    return romaji_string


def compare_hiragana_strings(input, expected):
    """Given two hiragana strings, compare how close the input text is to the expected test.
    Returns a value between 0 and 1."""
    grade = 1

    # how close is the length of the strings?
    length_difference = abs(len(expected) - len(input))
    grade -= length_difference / len(expected)

    for moji in input:
        if moji not in expected:
            grade *= HIRAGANA_NOT_FOUND_PENALTY

    return grade

def compare_romaji_strings(input, expected):
    """Given two hiragana strings, compare how close the input text is to the expected test.
    Returns a value between 0 and 1."""
    return SequenceMatcher(None, input, expected).ratio()

def split_word(input_text):
    """Given hiragana input, split into individual mora and return a tuple (word_array, mora_length)
    with the following information:
    word_array is an array of characters. Groups ゅ, ょ, and ゃ together with the previous mora.
    mora_length is the length of the word."""
    mora_length = 0
    word_array = []

    for char in input_text:
        if char in skip:
            i = mora_length - 1
            word_array[i] = word_array[i] + char
        else:
            word_array.append(char)
            mora_length += 1
    return (word_array, mora_length)