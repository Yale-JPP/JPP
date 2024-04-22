from gaussian_parse import GaussianParse
from utilities import split_word
import soundfile as sf

from settings import BASE_GRADE
from settings import PITCH_TOLERANCE, MINIMUM_DELTA
from settings import SELECTED_MODEL, CORRECT_LANGUAGE_WEIGHT, CORRECT_TEXT_WEIGHT

import whisper # consider local import to cut down on import time.
import utilities

import matplotlib.pyplot as plt
import numpy as np

from analysis import get_pitch_info, devoiced_check, get_bounds, within_bounds, error_calculation

filenames = [
    "一番.wav", "今週.wav", "先生.wav", "半分.wav", "大変.wav", "宿題.wav", "授業.wav", "文学.wav", "最近.wav", "毎日.wav",
    "生活.wav", "紹介.wav", "親切.wav", "野菜.wav", "世界.wav", "仕事.wav", "先週.wav", "単語.wav", "大学.wav", "専攻.wav",
    "推薦.wav", "料理.wav", "有名.wav", "毎朝.wav", "留学.wav", "経験.wav", "観光.wav", "鉛筆.wav", "両親.wav", "佐藤.wav",
    "全部.wav", "去年.wav", "天気.wav", "将来.wav", "携帯.wav", "新聞.wav", "本当.wav", "毎週.wav", "番号.wav", "練習.wav",
    "試合.wav", "電話.wav", "中国.wav", "作文.wav", "公園.wav", "台風.wav", "失礼.wav", "工学.wav", "政治.wav", "旅行.wav",
    "来年.wav", "気分.wav", "病気.wav", "美術.wav", "試験.wav", "電車.wav", "予報.wav", "便利.wav", "写真.wav", "喧嘩.wav",
    "学校.wav", "帽子.wav", "故障.wav", "旅館.wav", "来月.wav", "気温.wav", "病院.wav", "職業.wav", "財布.wav", "韓国.wav",
    "予定.wav", "俳優.wav", "出身.wav", "地獄.wav", "建物.wav", "教会.wav", "日本.wav", "来週.wav", "水泳.wav",
    "相談.wav", "胡椒.wav", "質問.wav", "音楽.wav", "予習.wav", "値段.wav", "剣道.wav", "地震.wav", "学生.wav",
    "彼女.wav", "教室.wav", "映画.wav", "正月.wav", "注文.wav", "砂糖.wav", "自分.wav", "連絡.wav", "高校.wav", "二本.wav",
    "元気.wav", "勉強.wav", "外国.wav", "安全.wav", "復習.wav", "散歩.wav", "時計.wav", "歴史.wav", "洗濯.wav", "研究.wav",
    "自由.wav", "週末.wav", "黒板.wav", "今度.wav", "兄弟.wav", "動物.wav", "大切.wav", "家族.wav", "成績.wav", "数学.wav",
    "時間.wav", "残念.wav", "温泉.wav", "社長.wav", "興味.wav", "都会.wav", "ご飯.wav", "今晩.wav", "先月.wav", "午前.wav",
    "大勢.wav", "家賃.wav", "掃除.wav", "文化.wav", "書道.wav", "毎年.wav", "漢字.wav", "神社.wav", "英語.wav", "野球.wav"
]


readings = [
    "いちばんです", "こんしゅうです", "せんせいです", "はんぶんです", "たいへんです", "しゅくだいです", "じゅぎょうです", "ぶんがくです", "さいきんです", "まいにちです",
    "せいかつです", "しょうかいです", "しんせつです", "やさいです", "せかいです", "しごとです", "せんしゅうです", "たんごです", "だいがくです", "せんこうです",
    "すいせんです", "りょうりです", "ゆうめいです", "まいあさです", "りゅうがくです", "けいけんです", "かんこうです", "えんぴつです", "りょうしんです", "さとうです",
    "ぜんぶです", "きょねんです", "てんきです", "しょうらいです", "けいたいです", "しんぶんです", "ほんとうです", "まいしゅうです", "ばんごうです", "れんしゅうです",
    "しあいです", "でんわです", "ちゅうごくです", "さくぶんです", "こうえんです", "たいふうです", "しつれいです", "こうがくです", "せいじです", "りょこうです",
    "らいねんです", "きぶんです", "びょうきです", "びじゅつです", "しけんです", "でんしゃです", "よほうです", "べんりです", "しゃしんです", "けんかです",
    "がっこうです", "ぼうしです", "こしょうです", "りょかんです", "らいげつです", "きおんです", "びょういんです", "しょくぎょうです", "さいふです", "かんこくです",
    "よていです", "はいゆうです", "しゅっしんです", "じごくです", "たてものです", "きょうかいです", "にほんです", "らいしゅうです", "すいえいです",
    "そうだんです", "こしょうです", "しつもんです", "おんがくです", "よしゅうです", "ねだんです", "けんどうです", "じしんです", "がくせいです",
    "かのじょです", "きょうしつです", "えいがです", "しょうがつです", "ちゅうもんです", "さとうです", "じぶんです", "れんらくです", "こうこうです", "にほんです",
    "げんきです", "べんきょうです", "がいこくです", "あんぜんです", "ふくしゅうです", "さんぽです", "とけいです", "れきしです", "せんたくです", "けんきゅうです",
    "じゆうです", "しゅうまつです", "こくばんです", "こんどです", "きょうだいです", "どうぶつです", "たいせつです", "かぞくです", "せいせきです", "すうがくです",
    "じかんです", "ざんねんです", "おんせんです", "しゃちょうです", "きょうみです", "とかいです", "ごはんです", "こんばんです", "せんげつです", "ごぜんです",
    "おおぜいです", "やちんです", "そうじです", "ぶんかです", "しょどうです", "まいとしです", "かんじです", "じんじゃです", "えいごです", "やきゅうです"
]



types = [
    2, 0, 3, 3, 0, 0, 1, 1, 0, 1, #
    0, 0, 1, 0, 1, 0, 0, 0, 0, 0, #
    0, 1, 0, 1, 0, 0, 0, 0, 1, 1, #
    1, 1, 1, 1, 0, 0, 0, 0, 3, 0, #
    0, 0, 0, 0, 0, 3, 2, 0, 0, 0, #
    0, 1, 0, 1, 2, 0, 0, 1, 0, 0, #
    0, 0, 0, 0, 1, 0, 0, 2, 0, 0, #
    0, 0, 0, 3, 2, 0, 2, 0, 0, #
    0, 2, 0, 1, 0, 0, 1, 0, 0, #
    1, 0, 0, 4, 0, 2, 0, 0, 0, 1,
    1, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    2, 0, 0, 1, 1, 0, 0, 1, 0, 0,
    0, 3, 0, 0, 1, 0, 1, 1, 1, 1,
    3, 1, 0, 1, 1, 0, 0, 1, 0, 0
]

# print(len(types), len(readings), len(filenames))

type_0s = []
type_1s = []
type_2s = []
type_3s = []
type_4s = []

# type_0s =  [('りょかんです', '旅館.wav', 0),
#             ('りょこうです', '旅行.wav', 0),
#             ('ねだんです', '値段.wav', 0),
#             ('しゃちょうです', '社長.wav', 0),
#             ('しあいです', '試合.wav', 0),
#             ('こしょうです', '故障.wav', 0),
#             ('よていです', '予定.wav', 0),
#             ('じしんです', '地震.wav', 0),
#             ('とかいです', '都会.wav', 0),
#             ('やきゅうです', '野球.wav', 0),
#             ('きおんです', '気温.wav', 0),
#             ('じぶんです', '自分.wav', 0),
#             ('よしゅうです', '予習.wav', 0),
#             ('しごとです', '仕事.wav', 0),
#             ('よほうです', '予報.wav', 0),
#             ('じかんです', '時間.wav', 0),
#             ('しゃしんです', '写真.wav', 0),
#             ('やさいです', '野菜.wav', 0)]

# type_1s = [('ごぜんです', '午前.wav', 1),
#            ('かぞくです', '家族.wav', 1),
#            ('びじゅつです', '美術.wav', 1),
#            ('にほんです', '二本.wav', 1),
#            ('しょどうです', '書道.wav', 1),
#            ('さとうです', '佐藤.wav', 1),
#            ('きぶんです', '気分.wav', 1),
#            ('せかいです', '世界.wav', 1),
#            ('やちんです', '家賃.wav', 1),
#            ('じゅぎょうです', '授業.wav', 1)]

# type_2s = [('にほんです', '日本.wav', 2),
#            ('じゆうです', '自由.wav', 2),
#            ('さとうです', '砂糖.wav', 2),
#            ('しけんです', '試験.wav', 2),
#            ('こしょうです', '胡椒.wav', 2)]

# type_3s = [('じごくです', '地獄.wav', 3)]

# type_4s = []

overall_grades = []
coefficients = []
pitch_grades = []
jump_accuracies = []
pattern_accuracies = []

def preliminary_pronunciation_check(filename, expected_text):
    """Uses whisper to check to see if the base level of pronunciation is good enough to be understood by Speech-to-Text AI.
    Will go through a series of checks to see if some standard expectations are met.
    Currently, those checks are making sure the model detects the spoken language as Japanese, and that the words are transcribed correctly.
    Note that filename and expected_text should be the full phrase, not the individual segmented phrases!
    Override for testing that also returns detected language, and detected phrase."""

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

    # decode the audio
    options = whisper.DecodingOptions()
    result = whisper.decode(model, mel, options)

    # start grading.
    if detected_language == "ja":
        grade += CORRECT_LANGUAGE_WEIGHT
        # result text will only ever be correct if in correct language, so nest.
        if result.text == expected_text:
            grade += CORRECT_TEXT_WEIGHT
        else:
            # japanese detected, incorrect word detected.
            result_hiragana = utilities.text_to_hiragana(result.text)
            expected_hiragana = utilities.text_to_hiragana(expected_text)

            grade += CORRECT_TEXT_WEIGHT * utilities.compare_hiragana_strings(result_hiragana, expected_hiragana)
    else:
        result_romaji = utilities.text_to_romaji(result.text)
        expected_romaji = utilities.text_to_romaji(expected_text)
        grade += CORRECT_LANGUAGE_WEIGHT * utilities.compare_romaji_strings(result_romaji, expected_romaji)

    return grade, detected_language, result.text

def calculate_grade(sf, sf_array, word, word_array, accent_type):
    """Grade the input sound clip given 5 arguments:
    Takes in the sound clip (sf), the full word (word), and the
    pitch accent pattern type.
    Also expects to be passed in a set of parallel arrays that has the sound clips and words broken
    down into its individual mora.
    Override for testing purposes. Returns (coefficient, grade)"""
    grade = 0
    data = preliminary_pronunciation_check(sf, word)
    coefficient = data[0]

    if coefficient != 0: # if it is worth it to grade the sound file
        # start with a base value that will be weighted according to the coefficient found.
        grade += BASE_GRADE
        result = grade_pitch_pattern(soundfiles=sf_array, accent_type=accent_type, word=word_array)
        grade += (100 - BASE_GRADE) * result[0]

    # gamma,
    return (coefficient, grade, data[1], data[2], result[1], result[2], result[3])


def grade_pitch_pattern(soundfiles, accent_type, word):
    """Expects an input of spliced soundfiles that refer to the word.
    For instance, gakusei-desu should be spliced ga-ku-se-i-de-su and passed in an array accordingly.
    accent_type refers to one of the four accent pattern types passed as an integer.
    word should be an array parallel with soundfiles that gives the spliced hiragana string.

    Override for testing purposes. Returns extra information as well."""
    grade = 0
    jump_accuracy = None
    pattern_accuracy = None
    coefficient = None

    pitches = []
    for mora in soundfiles:
        pitches.append(get_pitch_info(mora))

    if accent_type == 0: # heiban
        low_pitch = pitches[0]
        # check if 2nd mora is devoiced or not.
        if devoiced_check(word[1]) and len(word) > 2:
            high_pitch = pitches[2]
        else:
            high_pitch = pitches[1]
        delta = high_pitch - low_pitch

        if delta <= 0:
            jump_accuracy = 0
        elif delta <= MINIMUM_DELTA:
            jump_accuracy = error_calculation(expected=MINIMUM_DELTA, actual=delta)
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
        grade = (jump_accuracy + pattern_accuracy) / 2

    elif accent_type == 1: # high, drops gradually till end.
        high_pitch = pitches[0]

        pattern_accuracy = 0
        for i in range(len(pitches[1:])):
            lower_bound, upper_bound = get_bounds(high_pitch, PITCH_TOLERANCE)
            if pitches[i] <= lower_bound:
                pattern_accuracy += 1
                high_pitch = pitches[i]
            elif devoiced_check(word[i]):
                pattern_accuracy += 1
            else:
                pattern_accuracy += error_calculation(lower_bound, pitches[i])
                high_pitch = pitches[i] # to be kinder with grading, in case they accidentally went up.

        pattern_accuracy = pattern_accuracy / len(pitches[1:])
        grade = pattern_accuracy

    elif accent_type == 2: # low, high then gradually drops till end
        low_pitch = pitches[0]
        # check if 2nd mora is devoiced or not.
        if devoiced_check(word[1]) and len(word) > 2:
            high_pitch = pitches[2]
        else:
            high_pitch = pitches[1]
        delta = high_pitch - low_pitch

        if delta <= 0:
            jump_accuracy = 0
        elif delta <= MINIMUM_DELTA:
            jump_accuracy = error_calculation(expected=MINIMUM_DELTA, actual=delta)
        else:
            jump_accuracy = 1

        pattern_accuracy = 0
        for i in range(len(pitches[2:])):
            lower_bound, upper_bound = get_bounds(high_pitch, PITCH_TOLERANCE)
            if pitches[i] <= lower_bound:
                pattern_accuracy += 1
                high_pitch = pitches[i]
            elif devoiced_check(word[i]):
                pattern_accuracy += 1
            else:
                pattern_accuracy += error_calculation(lower_bound, pitches[i])
                high_pitch = pitches[i] # to be kinder with grading, in case they accidentally went up.
        pattern_accuracy = pattern_accuracy / len(pitches[2:])

        grade = (jump_accuracy + pattern_accuracy) / 2

    elif accent_type == 3: # low, high, high, then gradually drops till end.
        # requires a word of at least 3 mora to be type 3.
        low_pitch = pitches[0]
        # check if 2nd mora is devoiced or not.
        if devoiced_check(word[1]) and len(word) > 2:
            high_pitch = pitches[2]
            high_pitch2 = pitches[3]
        else:
            high_pitch = pitches[1]
            high_pitch2 = pitches[2]
        delta = high_pitch - low_pitch

        if delta <= 0:
            jump_accuracy = 0
        elif delta <= MINIMUM_DELTA:
            jump_accuracy = error_calculation(expected=MINIMUM_DELTA, actual=delta)
        else:
            jump_accuracy = 1

        pattern_accuracy = error_calculation(high_pitch, high_pitch2, PITCH_TOLERANCE)
        # high_pitch = max(high_pitch, high_pitch2) # nicer algorithm
        high_pitch = high_pitch2 # stricter algorithm

        for i in range(len(pitches[3:])):
            lower_bound, upper_bound = get_bounds(high_pitch, PITCH_TOLERANCE)
            if pitches[i] <= lower_bound:
                pattern_accuracy += 1
                high_pitch = pitches[i]
            elif devoiced_check(word[i]):
                pattern_accuracy += 1
            else:
                pattern_accuracy += error_calculation(lower_bound, pitches[i])
                high_pitch = pitches[i] # to be kinder with grading, in case they accidentally went up.
        pattern_accuracy = pattern_accuracy / (len(pitches[2:]) + 1)

        grade = (jump_accuracy + pattern_accuracy) / 2

    elif accent_type == 4: # low, hi, then drop on end of word (ie. on "de" of "desu")
        # assumes at least 2-mora word + de-su for 4 minimum mora.
        low_pitch = pitches[0]
        # check if 2nd mora is devoiced or not.
        if devoiced_check(word[1]) and len(word) > 2:
            high_pitch = pitches[2]
        else:
            high_pitch = pitches[1]
        delta = high_pitch - low_pitch

        if delta <= 0:
            jump_accuracy = 0
        elif delta <= MINIMUM_DELTA:
            jump_accuracy = error_calculation(expected=MINIMUM_DELTA, actual=delta)
        else:
            jump_accuracy = 1

        pattern_accuracy = 0
        for pitch in pitches[2:-2]: # cut at "desu." hard coded for 2-mora suffix, might need a dynamic approach later.
            if within_bounds(high_pitch, PITCH_TOLERANCE, pitch):
                # within the bounds. give perfect grade.
                pattern_accuracy += 1
            elif devoiced_check(word[pitches.index(pitch)]):
                # devoiced check comes before lower/upper bound comparisons
                pattern_accuracy += 1
            else:
                pattern_accuracy += error_calculation(high_pitch, pitch, PITCH_TOLERANCE)

        # reuse delta to calculate jump down from word to suffix.

        low_pitch = pitches[-2]
        # check if 2nd mora is devoiced or not.
        if devoiced_check(word[-3]):
            high_pitch = pitches[-3]
        else:
            high_pitch = pitches[-3]
        delta = high_pitch - low_pitch

        if delta <= 0:
            jump_accuracy = 0
        elif delta <= MINIMUM_DELTA:
            jump_accuracy += error_calculation(expected=MINIMUM_DELTA, actual=delta)
        else:
            jump_accuracy += 1

        jump_accuracy = jump_accuracy / 2 # average out over two expected jumps.

        # ensure last mora is in expected value compared to 2nd to last mora.
        lower_bound, upper_bound = get_bounds(low_pitch, PITCH_TOLERANCE)
        if pitches[-1] <= lower_bound:
            pattern_accuracy += 1
        elif devoiced_check(word[-1]):
            pattern_accuracy += 1
        else:
            pattern_accuracy += error_calculation(lower_bound, pitches[-1])

        pattern_accuracy = pattern_accuracy / (len(pitches[2:-2]) + 1) # add one for last drop pattern.
        grade = (jump_accuracy + pattern_accuracy) / 2

    return grade, jump_accuracy, pattern_accuracy, coefficient

def grade(word, accent_type, audio_file):
    sf_array = []
    word_array, mora_length = split_word(word)

    try:
        gp = GaussianParse(audio_file, word, mora_length)
        syllable_clips = gp.splice_audio()
    except IndexError:
        print(f"""error with {word} -- index error""")
        return
    except TypeError:
        print(f"""type error found with word {word}?""")
        return
    except:
        print(f"""some other error found with word {word}.""")
        return

    if len(syllable_clips) == mora_length:
        for i, syllable in enumerate(syllable_clips):
            export_filename = "output/" + word_array[i] + ".wav"
            # print(export_filename)
            sf.write(export_filename, syllable, 22050)
            # sf_array.append(syllable)
            sf_array.append(export_filename)
    else:
        print(f"""error with {word} -- incorrect syllable split""")
        return

    result = calculate_grade(audio_file, sf_array, word, word_array, accent_type)

    if result is None:
        return

    coeff = result[0]
    pitch_grade = result[1]
    detected_language = result[2]
    detected_phrase = result[3]
    jump_accuracy = result[4]
    pattern_accuracy = result[5]
    coeff2 = result[6]

    overall_grade = coeff * pitch_grade

    data = (coeff, pitch_grade, overall_grade, detected_language, detected_phrase, jump_accuracy, pattern_accuracy, coeff2)

    return data

def clear_arrays():
    overall_grades.clear()
    coefficients.clear()
    pitch_grades.clear()
    jump_accuracies.clear()
    pattern_accuracies.clear()

def save_grade_info(data):
    word = data[0] # word in hiragana.
    audio_file = "samples/" + data[1] # path to sound file. assumes samples folder is populated.
    accent_type = int(data[2])

    result = grade(word, accent_type, audio_file)
    # print(result)

    if result is None:
        coefficients.append(None)
        pitch_grades.append(None)
        overall_grades.append(None)
        jump_accuracies.append(None)
        pattern_accuracies.append(None)
        return

    coeff = result[0]
    pitch_grade = result[1]
    overall_grade = result[2]
    # detected_language = result[3]
    # detected_phrase = result[4]
    jump_accuracy = result[5]
    pattern_accuracy = result[6]
    # coeff2 = result[7]

    overall_grades.append(round(overall_grade / 100, 3))
    pitch_grades.append(round(pitch_grade / 100, 3))
    coefficients.append(round(coeff, 3))
    pattern_accuracies.append(round(pattern_accuracy, 3))
    if jump_accuracy is not None:
        jump_accuracies.append(round(jump_accuracy, 3))
    else:
        jump_accuracies.append(None)

def print_grade_info(data):
    word = data[0] # word in hiragana.
    audio_file = "samples/" + data[1] # path to sound file. assumes samples folder is populated.
    accent_type = int(data[2])

    result = grade(word, accent_type, audio_file)

    if result is None:
        return

    coeff = result[0]
    pitch_grade = result[1]
    overall_grade = result[2]
    detected_language = result[3]
    detected_phrase = result[4]
    jump_accuracy = result[5]
    pattern_accuracy = result[6]
    coeff2 = result[7]

    result_string = f"""{word} (Type {accent_type}):
Overall grade = {round(overall_grade, 3)}%
Coefficient γ = {round(coeff, 3)}
    Detected language = {detected_language}
    Detected phrase = {detected_phrase}
Pitch grade α = {round(pitch_grade / 100, 3)}
    """

    if jump_accuracy is not None:
        result_string += f"""   Jump accuracy j = {round(jump_accuracy, 3)}
        """

    result_string += f"""Pattern accuracy ρ = {round(pattern_accuracy, 3)}
    """

    if coeff2 is not None:
        result_string += f"""   Coefficient = {round(coeff2, 3)}"""

    print(result_string)

def plot(file_num):
    overall_grades_np = np.array(list(filter(lambda x: x is not None, overall_grades)))
    coefficients_np = np.array(list(filter(lambda x: x is not None, coefficients)))
    pitch_grades_np = np.array(list(filter(lambda x: x is not None, pitch_grades)))
    jump_accuracies_np = np.array(list(filter(lambda x: x is not None, jump_accuracies)))
    pattern_accuracies_np = np.array(list(filter(lambda x: x is not None, pattern_accuracies)))

    plt.clf()
    plt.hist(overall_grades_np, bins=[0.5, 0.6, 0.7, 0.8, 0.9, 1])
    plt.xlabel('Grades')
    plt.ylabel('Frequency')
    plt.title('Overall Grade')
    plt.savefig(f"data{str(file_num)}.png")
    file_num += 1

    plt.clf()
    plt.hist(pitch_grades_np, bins=[0.5, 0.6, 0.7, 0.8, 0.9, 1])
    plt.xlabel('Grades')
    plt.ylabel('Frequency')
    plt.title('Pitch Grade')
    plt.savefig(f"data{str(file_num)}.png")
    file_num += 1

    plt.clf()
    plt.hist(coefficients_np, bins=[0, 0.5, 0.6, 0.7, 0.8, 0.9, 1])
    plt.xlabel('Grades')
    plt.ylabel('Frequency')
    plt.title('Coefficients')
    plt.savefig(f"data{str(file_num)}.png")
    file_num += 1

    plt.clf()
    plt.hist(coefficients_np, bins=[0.8, 0.9, 1])
    plt.xlabel('Grades')
    plt.ylabel('Frequency')
    plt.title('Coefficients')
    plt.savefig(f"data{str(file_num)}.png")
    file_num += 1

    plt.clf()
    plt.hist(jump_accuracies_np, bins=[-.5,.5,1.5], ec="k")
    plt.xticks((0,1))
    plt.xlabel('Grades')
    plt.ylabel('Frequency')
    plt.title('Jump Accuracy')
    plt.savefig(f"data{str(file_num)}.png")
    file_num += 1

    plt.clf()
    plt.hist(pattern_accuracies_np, bins=[0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1])
    plt.xlabel('Grades')
    plt.ylabel('Frequency')
    plt.title('Pattern Accuracy')
    plt.savefig(f"data{str(file_num)}.png")
    file_num += 1

if __name__ == '__main__':
    file_num = 0

    dataset = []
    for i, word in enumerate(filenames):
        dataset.append((readings[i], word, types[i]))

    dataset = sorted(dataset, key=lambda data: data[2])

    for data in dataset:
        if data[2] == 0:
            type_0s.append(data)
        elif data[2] == 1:
            type_1s.append(data)
        elif data[2] == 2:
            type_2s.append(data)
        elif data[2] == 3:
            type_3s.append(data)
        elif data[2] == 4:
            type_4s.append(data)

    type_0s = []

    sorted_data = [type_0s, type_1s, type_2s, type_3s]
    for accent_type in sorted_data:
        print(accent_type)

    for i, accent_data in enumerate(sorted_data):
        for j, data in enumerate(accent_data):
            save_grade_info(data)
            # print(accent_data[j][0])
        print(f"""{overall_grades},
{pitch_grades},
{coefficients},
{jump_accuracies},
{pattern_accuracies}
              """)
        print(f"Finished accent type {i}.")
        clear_arrays()
        # plot(file_num)
        # file_num += 5