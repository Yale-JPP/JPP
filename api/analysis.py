import librosa
import numpy as np
from settings import PITCH_TOLERANCE, HOP_LENGTH, FMIN, FMAX, TYPE_0_EXPECTED_CHANGE
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

def grade_pitch_pattern(soundfiles, accent_type, word):
    """Expects an input of spliced soundfiles that refer to the word.
    For instance, gakusei-desu should be spliced ga-ku-se-i-de-su and passed in an array accordingly.
    accent_type refers to one of the four accent pattern types passed as an integer.
    word should be an array parallel with soundfiles that gives the spliced hiragana string."""
    mora_length = len(soundfiles)
    grade = 0
    pitches = []
    for mora in soundfiles:
        pitches.append(get_pitch_info(mora))

    if accent_type == 0: # heiban
        low_pitch = pitches[0]
        high_pitch = pitches[1]
        delta = high_pitch - low_pitch
        # 1 for perfect inputs, < 1 for smaller pitch changes than expected, < 1 for larger pitch changes than expected.
        lo_hi_jump_accuracy = min(TYPE_0_EXPECTED_CHANGE, delta) / max(delta, TYPE_0_EXPECTED_CHANGE)

        high_pitch_upper_bound = high_pitch + high_pitch * PITCH_TOLERANCE
        high_pitch_lower_bound = high_pitch - high_pitch * PITCH_TOLERANCE

        pattern_accuracy = 0
        for pitch in pitches[2:]:
            if pitch >= high_pitch_lower_bound and pitch <= high_pitch_upper_bound:
                # within the bounds. give perfect grade.
                pattern_accuracy += 1
            elif devoiced_check(word[pitches.index(pitch)]):
                # devoiced check comes before lower/upper bound comparisons
                pattern_accuracy += 1
            elif pitch < high_pitch_lower_bound:
                # lower than expected
                pattern_accuracy += pitch / high_pitch_lower_bound

            elif pitch > high_pitch_upper_bound:
                # higher than expected
                pattern_accuracy += high_pitch_upper_bound / pitch

        pattern_accuracy = pattern_accuracy / len(pitches[2:])
        grade += lo_hi_jump_accuracy * pattern_accuracy

    elif accent_type == 1: # high, drops till end.
        pass
    elif accent_type == 2:
        pass
    elif accent_type == 3:
        pass
    else:
        print("error")


    # def detect_pitch(y, sr, t):
    #     """Get pitch at time t."""
    #     index = magnitudes[:, t].argmax()
    #     pitch = pitches[index, t]

    #     return pitch

    # pitch = detect_pitch(y, sr, t=length/2)

    # print(pitch)

    # import matplotlib.pyplot as plt # remove later
    # # plt.scatter(pitches, magnitudes)

    # # for i in range(pitches.shape[1]): # for each column in pitches 2D array
    # #     pitch_column = pitches[:, i] # grab all the pitches at time frame 'i'
    # #     pitch_value = max(pitch_column) # grab max "dominant" pitch at 'i'
    # #     pitch_values.append(pitch_value)


    # # # Convert frame index to time
    # # times = librosa.times_like(pitches)

    # plt.figure(figsize=(10, 4))
    # plt.plot(times, pitch_values, label='Pitch (Hz)')
    # plt.xlabel('Time (s)')
    # plt.ylabel('Pitch (Hz)')
    # plt.title('Pitch of Human Voice')
    # plt.legend()
    # plt.show()
    # plot(pitch_values)

    # # using yin algorithm for faster runtime, since input soundfile should be a mostly monophonic audio signal
    # # note that yin uses FFTs internally.
    # pitch_o = aubio.pitch("yin", BUF_SIZE, HOP_SIZE, sr)
    # pitch_o.set_unit("hz") # midi will give us easier comparison for relative pitch, although Hz should also work. to test later.
    # pitch_o.set_tolerance(PITCH_TOLERANCE)

    # # iterate through input audio file
    # pitches = []
    # # confidence = []

    # total_frames = len(y) // HOP_SIZE
    # for frame_index in range(total_frames):
    #     start = frame_index * HOP_SIZE
    #     end = min((frame_index + 1) * HOP_SIZE, len(y)) # make sure not to go out of bounds
    #     samples = y[start:end]
    #     pitch_val = pitch_o(samples)[0]
    #     # print(pitch_o(samples))
    #     # if pitch_val != 0.0: # remove 0s as those are silent portions
    #     pitches.append(pitch_val)
    #     # confidence_val = pitch_o.get_confidence()
    #     # confidence.append(confidence_val)

    # print("Pitch values: ", pitches)
    # # # print("Confidence values:", confidence)
    # # print("Mora length (seconds): ", mora_length)
    # print(f"Average pitch value: {sum(pitches) / len(pitches)}",)

    # print(f"# of samples: {len(pitches)}")

    # plot(pitches)
    # return (pitches, mora_length)

# for testing.
