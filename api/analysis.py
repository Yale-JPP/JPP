from sys import exit, stderr
import os.path
import argparse
import librosa
import aubio
import numpy as np
import matplotlib.pyplot as plt
import whisper # consider local import to cut down on import time.
from difflib import SequenceMatcher

import utilities
from settings import *

# currently intended to be used in the command line while in development.

def init_parser():
    parser = argparse.ArgumentParser(allow_abbrev=False,
                                     description='sound analysis')
    parser.add_argument('filename', nargs='?', help='the filename of the soundfile to analyze', type=str)
    parser.add_argument('input_text', nargs='?', help='the word being said in the soundfile', type=str)
    return parser

def get_sound_info(filename, input_text):
    """Given an audio file to load, returns a tuple with (pitches, mora_length) where
    pitches is an array of pitch values, and mora_length is a length in seconds of the soundfile."""

    # note: y is audio signal in a 1D array
    # sr = sampling rate in Hz (ie. 44100 Hz)
    y, sr = librosa.load(filename)

    # mora length calculation
    mora_length = librosa.get_duration(y=y, sr=sr)

    # using yin algorithm for faster runtime, since input soundfile should be a mostly monophonic audio signal
    # note that yin uses FFTs internally.
    pitch_o = aubio.pitch("yin", BUF_SIZE, HOP_SIZE, sr)
    pitch_o.set_unit("midi") # midi will give us easier comparison for relative pitch, although Hz should also work. to test later.
    pitch_o.set_tolerance(PITCH_TOLERANCE)

    # iterate through input audio file
    pitches = []
    # confidence = []

    total_frames = len(y) // HOP_SIZE
    for frame_index in range(total_frames):
        start = frame_index * HOP_SIZE
        end = min((frame_index + 1) * HOP_SIZE, len(y)) # make sure not to go out of bounds
        samples = y[start:end]
        pitch_val = pitch_o(samples)[0]
        # print(pitch_o(samples))
        # if pitch_val != 0.0: # remove 0s as those are silent portions
        pitches.append(pitch_val)
        # confidence_val = pitch_o.get_confidence()
        # confidence.append(confidence_val)

    print("Pitch values: ", pitches)
    # # print("Confidence values:", confidence)
    # print("Mora length (seconds): ", mora_length)
    print("Average pitch value: ", sum(pitches) / len(pitches))

    print("# of samples: ", len(pitches))
    return (pitches, mora_length)

def compare_hiragana_strings(input, expected):
    """Given two hiragana strings, compare how close the input text is to the expected test.
    Returns a value between 0 and 1."""
    grade = 1

    # how close is the length of the strings?
    length_difference = len(expected) - len(input)
    grade -= length_difference / len(expected)

    for moji in input:
        if moji not in expected:
            grade *= HIRAGANA_NOT_FOUND_PENALTY

    return grade

def compare_romaji_strings(input, expected):
    """Given two hiragana strings, compare how close the input text is to the expected test.
    Returns a value between 0 and 1."""
    return SequenceMatcher(None, input, expected).ratio()

def preliminary_pronunciation_check(filename, expected_text):
    """Uses whisper to check to see if the base level of pronunciation is good enough to be understood by Speech-to-Text AI.
    Will go through a series of checks to see if some standard expectations are met.
    Currently, those checks are making sure the model detects the spoken language as Japanese, and that the words are transcribed correctly.
    Note that filename and expected_text should be the full phrase, not the individual segmented phrases!"""

    # grade assigned by whisper. starts at 0.
    grade = 0

    model = whisper.load_model(SELECTED_MODEL)

    # load audio and pad/trim it to fit 30 seconds
    audio = whisper.load_audio(filename)
    audio = whisper.pad_or_trim(audio)

    # make log-Mel spectrogram and move to the same device as the model
    mel = whisper.log_mel_spectrogram(audio).to(model.device)

    # detect the spoken language
    _, probs = model.detect_language(mel)
    detected_language = max(probs, key=probs.get)
    print(f"Detected language: {detected_language}")

    # decode the audio
    options = whisper.DecodingOptions()
    result = whisper.decode(model, mel, options)

    # print the recognized text
    print(result.text)

    # start grading.
    if detected_language == "ja":
        grade += CORRECT_LANGUAGE_WEIGHT
        # result text will only ever be correct if in correct language, so nest.
        if result.text == expected_text:
            grade += CORRECT_TEXT_WEIGHT
        else:
            # japanese detected, incorrect word detected.
            result_hiragana = utilities.text_to_hiragana(result.text)
            expected_hiragana = utilities.text_to_hiragana(expected_text)

            grade += CORRECT_TEXT_WEIGHT * compare_hiragana_strings(result_hiragana, expected_hiragana)
    else:
        result_romaji = utilities.text_to_romaji(result.text)
        expected_romaji = utilities.text_to_romaji(expected_text)
        grade += CORRECT_LANGUAGE_WEIGHT * compare_romaji_strings(result_hiragana, expected_hiragana)



def main():
    # current CLI interface lets us test individual sound files as well as the hard-coded example
    parser = init_parser()
    args = parser.parse_args()
    filename = args.filename
    input_text = args.input_text

    if filename is None or input_text is None:
        print("Incorrect parameters")
        return

    print("Currently reading: " + filename)
    if not os.path.isfile(filename):
        print("File not found")
        return
    else:
        grade = 0
        coefficient = preliminary_pronunciation_check(filename, input_text)
        if coefficient != 0: # if it is worth it to grade the sound file
            # start with a base value of 50. correct language bonus will scale this down to 50 * CORRECT_LANGUAGE_WEIGHT.
            grade += BASE_GRADE
            get_sound_info(filename)

    # # test gakusei-desu. used temporarily while in dev.
    # if filename is None:
    #     filename = ["samples/ga.wav",
    #                  "samples/ku.wav",
    #                  "samples/sei.wav",
    #                  "samples/de.wav",
    #                  "samples/su.wav"]
    #     for sf in filename:
    #         print("Currently reading: " + sf)
    #         res = get_sound_info(sf)
    #         print(res)
    #         print("")
    # # else do whatever file was requested
    # else:
    #     print("Currently reading: " + filename)
    #     if not os.path.isfile(filename):
    #         return "File not found"
    #     else:
    #         preliminary_pronunciation_check(filename, input_text)
    #         # get_sound_info(filename)

if __name__ == "__main__":
    main()