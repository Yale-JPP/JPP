import librosa
import aubio
from settings import BUF_SIZE, HOP_SIZE, PITCH_TOLERANCE

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
    print(f"Average pitch value: {sum(pitches) / len(pitches)}",)

    print(f"# of samples: {len(pitches)}")
    return (pitches, mora_length)
