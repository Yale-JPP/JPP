from ast import pattern
import librosa
import numpy as np
from settings import PITCH_TOLERANCE, HOP_LENGTH, FMIN, FMAX
from utilities import plot

COMMONLY_DEVOICED_MORA = ["く", "す"]

def get_pitch_info(filename):
    """Given an audio file to load, returns a pitch in midi."""
    # note: y is audio signal in a 1D array
    # sr = sampling rate in Hz (ie. 44100 Hz)
    y, sr = librosa.load(filename)

    pitches, magnitudes = librosa.core.piptrack(y=y, sr=sr, hop_length=HOP_LENGTH)
    # pitches, magnitudes = librosa.core.piptrack(y=y, sr=sr, hop_length=HOP_LENGTH, fmin=FMIN, fmax=FMAX)

    # get the pitches of the max indexes per time slice
    max_indexes = np.argmax(magnitudes, axis=0)
    pitches = pitches[max_indexes, range(magnitudes.shape[1])]

    median_pitch = pitches[len(pitches) // 2]
    # print(pitches)
    # print(pitches[len(pitches)//2])

    median_pitch_midi = librosa.hz_to_midi(median_pitch)

    return median_pitch_midi

def devoiced_check(word):
    """Check if a word contains a devoiced syllable and if it should be ignored in pitch accent calculations.
    In the future, it might be good if it also takes in the soundclip and checks if it was properly devoiced or not."""
    if word in COMMONLY_DEVOICED_MORA:
        return True
    else:
        return False

def get_bounds(target, tolerance):
    """Helper function that given a tolerance value and a target value, returns a tuple with
    the (lower_bound, upper_bound)."""
    upper_bound = target + target * tolerance
    lower_bound = target - target * tolerance
    return (lower_bound, upper_bound)

def within_bounds(target, tolerance, value):
    """Helper function that returns if the input value is within specifications."""
    lower, upper = get_bounds(target, tolerance)
    if value >= lower and value <= upper:
        return True
    else:
        return False

def error_calculation(expected, actual, tolerance=None):
    """Helper function that given an expected and actual value, calculates between (0, 1] how close
    the actual value was to the expected, with 1 being the most accurate and 0 being the least.
    If tolerance is passed in, instead handles a range of expected values."""
    if tolerance is None:
        return abs(expected - actual) / expected

    lower_bound, upper_bound = get_bounds(target=expected, tolerance=tolerance)

    if actual < lower_bound:
        # lower than expected
        return error_calculation(lower_bound, actual)
    else:
        # higher than expected
        return error_calculation(upper_bound, actual)

def grade_pitch_pattern(soundfiles, accent_type, word):
    """Expects an input of spliced soundfiles that refer to the word.
    For instance, gakusei-desu should be spliced ga-ku-se-i-de-su and passed in an array accordingly.
    accent_type refers to one of the four accent pattern types passed as an integer.
    word should be an array parallel with soundfiles that gives the spliced hiragana string."""
    grade = 0
    pitches = []
    for mora in soundfiles:
        pitches.append(get_pitch_info(mora))

    if accent_type == 0: # heiban
        low_pitch = pitches[0]
        # check if 2nd mora is devoiced or not.
        if devoiced_check(word[1]):
            high_pitch = pitches[2]
        else:
            high_pitch = pitches[1]
        delta = high_pitch - low_pitch

        if delta <= 0:
            jump_accuracy = 0
        # elif within_bounds(low_pitch, JUMP_TOLERANCE, high_pitch):
        #    pass
        else:
            jump_accuracy = 1

        pattern_accuracy = 0
        for pitch in pitches[2:]:
            if within_bounds(high_pitch, PITCH_TOLERANCE, pitch):
                # within the bounds. give perfect grade.
                pattern_accuracy += 1
            elif devoiced_check(word[pitches.index(pitch)]):
                # devoiced check comes before lower/upper bound comparisons
                pattern_accuracy += 1
            else:
                pattern_accuracy += error_calculation(high_pitch, pitch, PITCH_TOLERANCE)

        pattern_accuracy = pattern_accuracy / len(pitches[2:])
        print(jump_accuracy, pattern_accuracy)
        grade = jump_accuracy * pattern_accuracy

    elif accent_type == 1: # high, drops till end.
        high_pitch = pitches[0]
        pattern_accuracy = 0

        for i in range(len(pitches[1:])):
            lower_bound, upper_bound = get_bounds(high_pitch, PITCH_TOLERANCE)
            if pitches[i] <= upper_bound * high_pitch:
                pattern_accuracy += 1
                high_pitch = pitches[i]
            elif devoiced_check(word[i]):
                pattern_accuracy += 1
            else:
                pattern_accuracy += error_calculation(upper_bound * high_pitch, pitches[i])
                high_pitch = pitches[i] # to be kinder with grading, in case they accidentally went up.

        pattern_accuracy = pattern_accuracy / len(pitches[1:])
        print(pattern_accuracy)
        grade = pattern_accuracy

    elif accent_type == 2:
        pass
    elif accent_type == 3:
        pass
    else:
        print("Invalid accent type.")

    return grade

# for testing.
soundfiles = ["samples/ga.wav", "samples/ku.wav", "samples/sei.wav", "samples/de.wav", "samples/su.wav"]
accent_type = 0
word = ["が", "く", "せい", "で", "す"]
result = grade_pitch_pattern(soundfiles, accent_type, word)