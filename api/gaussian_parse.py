import os
import math

import librosa
import librosa.display
import soundfile as sf

import scipy
import numpy as np
import matplotlib.pyplot as plt
from utilities import vowel, skip, data


# I have the word -> I have the # of mora -> dipthong syllables count as one -> do below step
# Gaussian -> # of gaussian is # of mora -> find peaks and get the lowest point in between to get timestamps
# Separate dipthong later

# Problem with 自由, maybe look at points of inflection as well?
# 試合、試験
# Doesn't perform well when vowels are next to each other, thus shi-a-i is bad, three vowels next to each other

# Problem with the way we split - maybe have someway to make the vowels the same length, but make the portion of the consonant longer
# Need to see if this happens often

# Find a way to handle っ. Maybe if there is a plateau for a while, then split properly

# What I need, basivally make a page with words, with the words have the associated mora and furigana so that when
# We look at the word, we can determine the mora and furigana for the gaussian parse

class GaussianParse():
    """
    Takes the directory and file name of an audio file.
    Makes the waveform of the audio file in order to find the
    Guassian filtered curve, the peaks of that curve, and the
    dips of that curve. Can separate the audio file into syllables and
    plot the graph.
    """
    def __init__(self, file, furigana, mora):
    # def __init__(self, data, sr, furigana, mora):
        # Create the path and find the word
        # self._path = os.path.join(dir, file)
        # self._kanji = file[:-4]

        # --------FOR TESTING PURPOSES---------------
        self._furigana = furigana
        self._mora = mora
        # -------------------------------------------

        # Load the waveform
        self._original, self._sampling_rate = librosa.load(file)
        S_full, phase = librosa.magphase(librosa.stft(self._original))
        S_filter = librosa.decompose.nn_filter(S_full,
                                       aggregate=np.median,
                                       metric='cosine',
                                       width=int(librosa.time_to_frames(.1, sr=self._sampling_rate)))
        S_filter = np.minimum(S_full, S_filter)
        margin_v = 10
        power = 2

        mask_v = librosa.util.softmask(S_full - S_filter,
                                    margin_v * S_filter,
                                    power=power)

        S_foreground = mask_v * S_full
        new_y = librosa.istft(S_foreground*phase)
        sf.write('extracted.wav', new_y, self._sampling_rate)
        # self._original = data
        # self._sampling_rate = sr
        # print(self._original.shape)
        self._original, self._index = librosa.effects.trim(new_y, top_db=40)
        # print(self._original.shape)
        self._waveform = np.array(self._original, copy=True)
        self._waveform[self._waveform < 0] = 0

        # Get the time values of each point on the waveform
        self._dur = librosa.get_duration(y=self._waveform)
        self._time = np.linspace(start=0, stop=self._dur, num=math.floor(self._dur * self._sampling_rate))

        # Calculate the peaks from the gaussian filtered data
        self._gauss_filt = scipy.ndimage.gaussian_filter1d(self._waveform, sigma=500)
        self._peaks, _ = scipy.signal.find_peaks(self._gauss_filt, height=.01)

        # Calculate the dips
        self._dips = []
        for i in range(len(self._peaks) - 1):
            self._dips.append(np.where(self._gauss_filt == min(self._gauss_filt[self._peaks[i]:self._peaks[i+1]]))[0][0])
        self._dips = np.array(self._dips)

    def splice_audio(self):
        """
        Splices and separates the audio into syllables and outputs them in a new file.
        """
        if len(self._dips) + 1 < self._mora - 1:
            # Not all syllables in the word has been cut
            # print(self._dips)
            i = 0
            dip_indexer = 0
            while i < len(self._furigana[:-2]):
                # If the moji combines with the previous moji to make one mora
                if self._furigana[i] in skip:
                    i += 1
                    continue
                # print("Current moji = " + self._furigana[i])
                # print("Current i = " + str(i))
                # If there is a vowel that is not the first letter
                if self._furigana[i] in vowels and i != 0:
                    # Count the number of vowels to split the clip by
                    # start_i = i
                    vowel_chain = 1
                    # print("start_i = " + str(start_i))
                    while self._furigana[i + 1] in vowels:
                        vowel_chain += 1
                        i += 1
                    # vowel_chain = i - start_i + 1
                    # print("vowel chain = " + str(vowel_chain))
                    # Find the duration that we should split the clip by
                    bad_dip_end = self._dips[dip_indexer - 1]
                    # print("bad_dip_end = " + str(bad_dip_end))
                    bad_dip_start = 0 if dip_indexer - 2 < 0 else self._dips[dip_indexer - 2]
                    # print("bad_dip_start = " + str(bad_dip_start))
                    mora_dur = (bad_dip_end - bad_dip_start) // (vowel_chain + 1)
                    # print("mora_dur = " + str(mora_dur))
                    # Insert the newly broken clips into self._dips
                    for j in range(vowel_chain):
                        # print("at index " + str(dip_indexer + j) + " inserting " + str(bad_dip_start + (mora_dur * (j + 1))))
                        self._dips = np.insert(self._dips, (dip_indexer - 1) + j, bad_dip_start + (mora_dur * (j + 1)))
                        # print(self._dips)
                i += 1
                dip_indexer += 1

        # print(self._dips)

        if len(self._dips) + 1 == self._mora - 1:
            # Every syllable besides です has been cut
            desu = self._dips[-1]
            half_point = desu + ((self._waveform.size - desu) // 3)
            self._dips = np.append(self._dips, [half_point])

        t1 = 0
        clips = []
        for i, end_timestamp in enumerate(self._dips):
            # export_filename = "output/" + self._kanji + str(i) + ".wav"
            newAudio = self._original[t1:end_timestamp]
            # sf.write(export_filename, newAudio, self._sampling_rate)
            clips.append(newAudio)
            t1 = end_timestamp

        # export_filename = "output/" + self._kanji + str(self._mora - 1) + ".wav"
        newAudio = self._original[t1:]
        clips.append(newAudio)
        return clips
        # sf.write(export_filename, newAudio, self._sampling_rate)

    def plot_waves(self):
        """
        Plots all the waves and graphs.
        """
        fig, axes = plt.subplots(ncols=2, figsize=(15, 5))
        # fig.canvas.manager.set_window_title(self._kanji)

        axes[0].plot(self._time, self._gauss_filt, label='gaussian filter')
        axes[1].plot(self._time, self._waveform, label='altered data')

        axes[0].plot(self._time[self._peaks], self._gauss_filt[self._peaks], "x", label='peaks')
        axes[0].plot(self._time[self._dips], self._gauss_filt[self._dips], "x", label='dips')

        # librosa.display.waveshow(self._original, sr=self._sampling_rate)
        axes[0].legend()
        axes[1].legend()
        plt.savefig("output.jpg")
        # plt.show()

# if __name__ == "__main__":

#     dir_name = '1+2 Noun/'
#     # entries = os.listdir(dir_name)

#     for entry in data:
#     # for entry in entries:
#         # print(entry[:-4], end=" ")
#         gp = GaussianParse(dir_name, entry[0] + ".wav", entry[1], entry[2])
#         gp.splice_audio()
#         gp.plot_waves()
#     # gp = GaussianParse('1+2 Noun/', '世界.wav', "せかいです", 5)
#     # gp.splice_audio()
#     # gp.plot_waves()
