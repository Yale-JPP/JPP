from gaussian_parse import GaussianParse
from grading import calculate_grade
from utilities import split_word
import soundfile as sf

def grade(word, accent_type, audio_file):
    sf_array = []
    word_array, mora_length = split_word(word)

    gp = GaussianParse(audio_file, word, mora_length)
    syllable_clips = gp.splice_audio()

    if len(syllable_clips) == mora_length:
        for i, syllable in enumerate(syllable_clips):
            export_filename = "output/" + word[i] + ".wav"
            # print(export_filename)
            sf.write(export_filename, syllable, 22050)
            # sf_array.append(syllable)
            sf_array.append(export_filename)
    else:
        print("error: incorrect number of syllables.")
        return

    result = calculate_grade(audio_file, sf_array, word, word_array, accent_type)

    result = round(result, 1)

    return result

if __name__ == '__main__':
    word = "" # word in hiragana.
    accent_type = 0
    audio_file = "" # path to sound file.

    result = grade(word, accent_type, audio_file)
    print(result)