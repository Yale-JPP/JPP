import numpy as np
import math

import librosa
import librosa.display
import matplotlib.pyplot as plt
import soundfile as sf

"""
Given the kanji, find the audio file and split it on the given mora_length
Only woks if mora length is known, but since we have given words, we know
what the length should be
"""
class DurationParse():
    def __init__(self, kanji, mora_length, file_path):
        self._kanji = kanji

        self._original, self._sampling_rate = librosa.load(file_path)
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

        _, self._index = librosa.effects.trim(new_y, top_db=40)
        # print(self._index)
        self._original = self._original[self._index[0]:self._index[1]]

        duration = librosa.get_duration(y=self._original)
        self._mora_duration = duration / float(mora_length)

        self._mora_length = mora_length
        self._time_divisions = self._split()
    
    # Currently only works for the 1+2 Noun file
    def _split(self):
        time = 0
        divisions = []
        for i in range(self._mora_length):
            time += self._mora_duration
            divisions.append(time)
        return divisions

    def get_divisions(self):
        """Returns the end timestamp of each parsed mora"""
        return self._time_divisions

    def get_parsed_clips(self):
        """Exports new wav files of the parsed mora"""
        t1 = 0
        for i, end_timestamp in enumerate(self._time_divisions):
            end = math.floor(end_timestamp * self._sampling_rate)
            export_filename = "output/" + self._kanji + "_dp" + str(i) + ".wav"
            newAudio = self._original[t1:end]
            sf.write(export_filename, newAudio, self._sampling_rate)
            t1 = end

    def get_original_clip_timestamps(self):
        """Returns list of timestamps of when each mora starts, and when the last one ends"""
        res = [float(self._index[0]) / self._sampling_rate]
        for i in range(self._mora_length):
            res.append(res[i] + self._mora_duration)
        return res
        

# word_list = ["世界", "予報", "旅行", "気分", "自分", "自由", "野球", "都会"]
# word_list = ['一番', '両親', '中国', '今晩', '今週', '作文', '先生', '兄弟', '半分']
word_list = ['半分']

if __name__ == "__main__":
    for kanji in word_list:
        file_path = "2+2 Noun/" + kanji + ".wav"
        separated = DurationParse(kanji, 5, file_path)
        print(separated.get_divisions())
        separated.get_parsed_clips()

        print(separated.get_original_clip_timestamps())

        times = separated.get_divisions()
        fig = plt.figure()
        librosa.display.waveshow(separated._original, sr=separated._sampling_rate, label='waveform')
        plt.vlines(x = times, ymin = -.15, ymax = .15,
            colors = 'purple',
            ls='--',
            label = 'end timestamp')
        plt.legend()
        plt.xlabel("Time")
        plt.ylabel("Amplitude")
        plt.show()