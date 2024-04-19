from gaussian_parse import GaussianParse
from grading import calculate_grade
from utilities import split_word
import soundfile as sf

dataset = [
    ("ごぜんです", "午前.wav", 1),
    ("りょかんです", "旅館.wav", 0),
    ("にほんです", "日本.wav", 2),
    ("りょこうです", "旅行.wav", 0),
    ("ねだんです", "値段.wav", 0),
    ("かぞくです", "家族.wav", 1),
    ("しゃちょうです", "社長.wav", 0),
    ("じゆうです", "自由.wav", 2),
    ("しあいです", "試合.wav", 0),
    ("こしょうです", "故障.wav", 0),
    ("よていです", "予定.wav", 0),
    ("じしんです", "地震.wav", 0),
    ("さとうです", "砂糖.wav", 2),
    ("びじゅつです", "美術.wav", 1),
    ("じごくです", "地獄.wav", 3),
    ("とかいです", "都会.wav", 0),
    ("きょねんです", "去年.wav", 1),
    ("にほんです", "二本.wav", 1),
    ("やきゅうです", "野球.wav", 0),
    ("きおんです", "気温.wav", 0),
    ("じぶんです", "自分.wav", 0),
    ("しょどうです", "書道.wav", 1),
    ("よしゅうです", "予習.wav", 0),
    ("さとうです", "佐藤.wav", 1),
    ("きぶんです", "気分.wav", 1),
    ("せかいです", "世界.wav", 1),
    ("しごとです", "仕事.wav", 0),
    ("よほうです", "予報.wav", 0),
    ("しけんです", "試験.wav", 2),
    ("やちんです", "家賃.wav", 1),
    ("じかんです", "時間.wav", 0),
    ("しゃしんです", "写真.wav", 0),
    ("やさいです", "野菜.wav", 0),
    ("こしょうです", "胡椒.wav", 2),
    ("じゅぎょうです", "授業.wav", 1)
]

def grade(word, accent_type, audio_file):
    sf_array = []
    word_array, mora_length = split_word(word)
    # print(word_array, mora_length)

    gp = GaussianParse(audio_file, word, mora_length)
    syllable_clips = gp.splice_audio()
    # print(len(syllable_clips))

    if len(syllable_clips) == mora_length:
        for i, syllable in enumerate(syllable_clips):
            export_filename = "output/" + word[i] + ".wav"
            # print(export_filename)
            sf.write(export_filename, syllable, 22050)
            # sf_array.append(syllable)
            sf_array.append(export_filename)
    else:
        print(f"error with {word} -- incorrect syllable split")
        return

    result = calculate_grade(audio_file, sf_array, word, word_array, accent_type)

    result = round(result, 1)

    return result



if __name__ == '__main__':
    # individual test.
    # data = dataset[0]
    # word = data[0] # word in hiragana.
    # audio_file = "samples/" + data[1] # path to sound file. assumes samples folder is populated.
    # accent_type = int(data[2])

    # result = grade(word, accent_type, audio_file)
    # print(f"{result} ({accent_type}), {result}%")

    # full test
    for data in dataset:
        word = data[0] # word in hiragana.
        audio_file = "samples/" + data[1] # path to sound file. assumes samples folder is populated.
        accent_type = int(data[2])

        result = grade(word, accent_type, audio_file)
        print(f"{result} ({accent_type}), {result}%")
