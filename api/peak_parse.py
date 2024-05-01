import librosa
import librosa.display
import soundfile as sf

import scipy
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.ticker import FormatStrFormatter
from utilities import vowels, skip, data

vowels = ['あ', 'い', 'う', 'え', 'お', 'ん']
skip = ['ゃ', 'ゅ', 'ょ']


class PeakParse():
    """
    Takes the file of an audio file and makes a waveform.
    Guassian filters the curve to find the peaks and dips of that curve.
    Can separate the audio file into syllables and plot the graph. 
    """
    # def __init__(self, dir, file, furigana, mora):
    def __init__(self, file, furigana, mora):    
        # Create the path and find the word
        self._furigana = furigana
        self._mora = mora
        
        # Load the waveform
        self._original, self._sampling_rate = librosa.load(file)
        
        # Voice Isolate
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

        # Trim the silence from the beginning and end
        self._trimmed, self._index = librosa.effects.trim(new_y, top_db=40)
        self._original = self._original[self._index[0]: self._index[1]]

        # Alter the wave_form's data
        self._waveform = np.array(self._trimmed, copy=True)
        self._waveform[self._waveform < 0] = 0
        
        # Get the time values of each point on the waveform
        self._dur = librosa.get_duration(y=self._waveform)
        self._time = np.linspace(start=0, stop=self._dur, num=self._waveform.shape[0])

        # Calculate the peaks from the gaussian filtered data
        self._gauss_filt = scipy.ndimage.gaussian_filter1d(self._waveform, sigma=500)
        max = np.max(self._gauss_filt)
        self._gauss_filt /= max

        # Get the number of double vowels
        num_of_double_vowels = 0
        for i in range(len(furigana)):
            if i == 0:
                continue
            else:
                if furigana[i] in vowels:
                    num_of_double_vowels += 1

        # The expected peaks we get are on for each mora minus the devoiced vowels and double vowels
        # We subtract one for /desu/ and by the number of souble vowels
        # Then we repeatedly try lower peak_heights until we get the right amount of peaks
        # There is the issue of getting more peaks than we want
        peak_height = .005
        self._peaks, _ = scipy.signal.find_peaks(self._gauss_filt, height=(peak_height / max))
        while len(self._peaks) < (mora - 1 - num_of_double_vowels):
            if peak_height == 0:
                break
            peak_height -= .001
            self._peaks, _ = scipy.signal.find_peaks(self._gauss_filt, height=(peak_height / max))

        # Calculate the dips
        self._dips = []
        for i in range(len(self._peaks) - 1):
            self._dips.append(np.where(self._gauss_filt == min(self._gauss_filt[self._peaks[i]:self._peaks[i+1]]))[0][0])
        self._dips = np.array(self._dips)
        self._splice_audio()

    def _splice_audio(self):
        """
        Splices and separates the audio into syllables
        """
        # Not all syllables in the word has been cut
        if len(self._dips) + 1 < self._mora - 1:
            i = 0
            dip_indexer = 0
            while i < len(self._furigana[:-2]):
                # If the moji is small /ya/, /yu/, /yo/
                if self._furigana[i] in skip:
                    i += 1
                    continue
                # If there is a vowel that is not the first letter
                if self._furigana[i] in vowels and i != 0:
                    # Count the number of vowels to split the clip by
                    vowel_chain = 1
                    while self._furigana[i + 1] in vowels:
                        vowel_chain += 1
                        i += 1

                    # Find the duration that we should split the clip by
                    bad_dip_end = len(self._gauss_filt) if dip_indexer - 1 >= len(self._dips) else self._dips[dip_indexer - 1]
                    bad_dip_start = 0 if dip_indexer - 2 < 0 else self._dips[dip_indexer - 2]
                    mora_dur = (bad_dip_end - bad_dip_start) // (vowel_chain + 1)

                    # Insert the newly broken clips into self._dips
                    for j in range(vowel_chain):
                        self._dips = np.insert(self._dips, (dip_indexer - 1) + j, bad_dip_start + (mora_dur * (j + 1)))
                i += 1
                dip_indexer += 1
        
        # Every syllable besides desu has been cut
        if len(self._dips) + 1 == self._mora - 1:
            desu = self._dips[-1]
            half_point = desu + ((self._waveform.size - desu) // 2)
            self._dips = np.append(self._dips, [half_point])

    def parse_clips(self):
        """
        Returns the clips of audio that were split.
        """
        clips = []
        t1 = 0
        for i, end_timestamp in enumerate(self._dips):
            # export_filename = "output/" + self._furigana + "_gp" + str(i) + ".wav"
            newAudio = self._original[t1:end_timestamp]
            clips.append(newAudio)
            # sf.write(export_filename, newAudio, self._sampling_rate)
            t1 = end_timestamp
        
        # export_filename = "output/" + self._furigana + "_gp" + str(self._mora - 1) + ".wav"
        newAudio = self._original[t1:]
        clips.append(newAudio)
        # sf.write(export_filename, newAudio, self._sampling_rate)
        return clips
    
    def plot_waves(self):
        """
        Plots all the waves and graphs. For research purposes. 
        """
        gs = gridspec.GridSpec(2, 2)

        fig = plt.figure(figsize=(8.8, 6))
        ax1 = fig.add_subplot(gs[0, 0]) # row 0, col 0
        librosa.display.waveshow(self._original, sr=self._sampling_rate, ax=ax1, color="#1f77b4")
        ax1.xaxis.set_major_formatter(FormatStrFormatter('%g'))
        ax1.set_title("Waveform")
        plt.xlabel("Time")
        plt.ylabel("Amplitude")

        ax2 = fig.add_subplot(gs[0, 1]) # row 0, col 1
        ax2.plot(self._time, self._waveform)
        ax2.set_title("Altered Data")
        plt.xlabel("Time")
        plt.ylabel("Amplitude")

        ax3 = fig.add_subplot(gs[1, :]) # row 1, span all columns
        ax3.plot(self._time, self._gauss_filt, label='Gaussian Filter')
        ax3.plot(self._time[self._peaks], self._gauss_filt[self._peaks], "x", label='peaks')
        ax3.plot(self._time[self._dips], self._gauss_filt[self._dips], "x", label='dips')
        ax3.legend()
        plt.xlabel("Time")
        plt.ylabel("Amplitude")

        plt.savefig("output.jpg")
        # plt.show()

    def get_original_clip_timestamps(self):
        """
        Returns list of timestamps of when each mora starts, and when the last one ends.
        For research purposes. 
        """
        res = [float(self._index[0]) / self._sampling_rate]
        for idx in self._dips:
            res.append(res[0] + (float(idx) / self._sampling_rate))
        res.append(float(self._index[1]) / self._sampling_rate)
        return res