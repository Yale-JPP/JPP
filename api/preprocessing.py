from difflib import SequenceMatcher
import whisper # consider local import to cut down on import time.
from settings import SELECTED_MODEL, CORRECT_LANGUAGE_WEIGHT, CORRECT_TEXT_WEIGHT, HIRAGANA_NOT_FOUND_PENALTY
import utilities

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

            grade += CORRECT_TEXT_WEIGHT * utilities.compare_hiragana_strings(result_hiragana, expected_hiragana)
    else:
        result_romaji = utilities.text_to_romaji(result.text)
        expected_romaji = utilities.text_to_romaji(expected_text)
        grade += CORRECT_LANGUAGE_WEIGHT * utilities.compare_romaji_strings(result_romaji, expected_romaji)

    return grade