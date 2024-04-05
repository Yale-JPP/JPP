import pykakasi
import numpy as np
import matplotlib.pyplot as plt

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