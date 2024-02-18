from sys import exit, stderr
import argparse
import librosa
import aubio

# currently intended to be used in the command line while in development.

def init_parser():
    parser = argparse.ArgumentParser(allow_abbrev=False,
                                     description='sound analysis')
    parser.add_argument('soundfile', nargs='?', help='the soundfile to analyze', type=str)
    return parser


def get_average_pitch(filename):
    """Given an audio file to load, returns a tuple with (pitches, mora_length) where
    pitches is an array of pitch values, and mora_length is a length in seconds of the soundfile."""
    # note: y is audio signal in a 1D array
    # sr = sampling rate in Hz (ie. 44100 Hz)
    y, sr = librosa.load(filename)

    # mora length calculation
    mora_length = librosa.get_duration(y=y, sr=sr)

    buf_size = 1024 # higher value means more frequency resolution
    hop_size = 128 # lower value means larger rate of sampling

    # using yin algorithm for faster runtime, since input soundfile should be a mostly monophonic audio signal
    pitch_o = aubio.pitch("yin", buf_size, hop_size, sr)
    pitch_o.set_unit("midi") # midi will give us easier comparison for relative pitch, although Hz should also work. to test later.
    pitch_o.set_tolerance(0.8)

    # iterate through input audio file
    pitches = []
    # confidence = []

    total_frames = len(y) // hop_size
    for frame_index in range(total_frames):
        start = frame_index * hop_size
        end = min((frame_index + 1) * hop_size, len(y)) # make sure not to go out of bounds
        samples = y[start:end]
        pitch_val = pitch_o(samples)[0]
        # print(pitch_o(samples))
        if pitch_val != 0.0: # remove 0s as those are silent portions
            pitches.append(pitch_val)
        # confidence_val = pitch_o.get_confidence()
        # confidence.append(confidence_val)

    # print("Pitch values: ", pitches)
    # # print("Confidence values:", confidence)
    # print("Mora length (seconds): ", mora_length)
    # print("Average pitch value: ", sum(pitches) / len(pitches))
    return (pitches, mora_length)


def main():
    # current CLI interface lets us test individual sound files as well as the hard-coded example
    parser = init_parser()
    args = parser.parse_args()
    soundfile = args.soundfile

    # test gakusei-desu
    if soundfile is None:
        soundfile = ["samples/ga.wav",
                     "samples/ku.wav",
                     "samples/sei.wav",
                     "samples/de.wav",
                     "samples/su.wav"]
        for sf in soundfile:
            print("Currently reading: " + sf)
            res = get_average_pitch(sf)
            print(res)
            print("")
    # else do whatever file was requested
    else:
        print("Currently reading: " + soundfile)
        print(get_average_pitch(soundfile))


if __name__ == "__main__":
    main()