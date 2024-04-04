from sys import exit, stderr
import os.path
import argparse
import librosa
import aubio
import numpy as np
import matplotlib.pyplot as plt
import whisper # consider local import to cut down on import time.

# currently intended to be used in the command line while in development.

# ~~~~~~~~~~~ PARAMETERS THAT AFFECT GRADING ~~~~~~~~~~~
SELECTED_MODEL = "base" # model type used for whisper. one of "tiny", "base", "small", "medium", and "large".
CORRECT_LANGUAGE_WEIGHT = 0.6 # weight given to an answer that gets the correct language detected.
CORRECT_TEXT_WEIGHT = 0.4 # weight given to an answer that gets the correct input text detected.
BUF_SIZE = 1024 # higher value means more frequency resolution
HOP_SIZE = 128 # lower value means larger rate of sampling
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def init_parser():
    parser = argparse.ArgumentParser(allow_abbrev=False,
                                     description='sound analysis')
    parser.add_argument('filename', nargs='?', help='the filename of the soundfile to analyze', type=str)
    parser.add_argument('input_text', nargs='?', help='the word being said in the soundfile', type=str)
    return parser

def get_sound_info(filename):
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
    pitch_o.set_tolerance(0.8)

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
    plot(pitches)
    return (pitches, mora_length)


def plot(pitches):
    """Given a set of pitches, plot them equally spaced in time to see a visualization of the pitch over time."""
    time_axis = np.arange(len(pitches))
    plt.scatter(time_axis, pitches)

    plt.ylabel("Pitch")
    plt.title("Pitch vs. Time")

    plt.show()

def preliminary_pronunciation_check(filename, input_text):
    """Uses whisper to check to see if the base level of pronunciation is good enough to be understood by Speech-to-Text AI.
    Will go through a series of checks to see if some standard expectations are met."""

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
        grade += 0.6
        # result text will only ever be correct if in correct language, so nest.
        if result.text == input_text:
            grade += 0.4
        else:
            # partial credit here perhaps?
            pass

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
            grade += 50
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