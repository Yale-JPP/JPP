import time
import subprocess
import io
import wave
from base64 import b64decode
from flask import Flask, request, jsonify
from gaussian_parse import GaussianParse
from grading import calculate_grade
from utilities import split_word
import soundfile as sf

app = Flask(__name__)

@app.route('/time')
def get_current_time():
    return {'time': time.time()}

@app.route('/parse-syllables', methods=['POST'])
def parse_syllables():
    # audio_file = request.files.get('audio_data')
    # file_type = request.form.get("type", "webm")
    # print(audio_file)
    # print(file_type)
    audio = str(request.json["audio"])
    audio = audio.split(",")[1]
    audio = b64decode(audio)
    # print(audio)
    # audio = str(request.json["audio"])
    # audio = b64decode(audio)

    p = subprocess.run(["ffmpeg", "-y", "-i", "-", "-vn", "audio.wav"], input=audio, capture_output=True)
    if p.returncode != 0:
        print("ffmpeg:", p.returncode)
        print(p.stdout)
        print(p.stderr)
        return {"error": "ffmpeg failed to convert audio"}, 500
    wav_path = "audio.wav"
    # data, samplerate = sf.read(io.BytesIO(audio))

    gp = GaussianParse(wav_path, "しごとです", 5)
    syllable_clips = gp.splice_audio()
    # gp.plot_waves()
    for i, syllable in enumerate(syllable_clips):
        export_filename = "output/" + "仕事" + str(i) + ".wav"
        sf.write(export_filename, syllable, 22050)

    return jsonify("it works"), 200

@app.route('/grade', methods=['POST'])
def grade():
    # data = request.form
    # sf = data.get('sf')
    # word = data.get('word')
    # accent_type = data.get('accent_type')
    word = request.form.get('word')
    accent_type = request.form.get('accent_type')
    audio_file = request.form.get('sf')

    sf_array = []
    word_array = []

    if not (word and accent_type and audio_file):
        return jsonify({'error': 'Missing required data in request'}), 400

    word_array, mora_length = split_word(word)

    audio = str(audio_file)
    audio = audio.split(",")[1]
    audio = b64decode(audio)
    # print(audio)
    # audio = str(request.json["audio"])
    # audio = b64decode(audio)

    p = subprocess.run(["ffmpeg", "-y", "-i", "-", "-vn", "audio.wav"], input=audio, capture_output=True)
    if p.returncode != 0:
        print("ffmpeg:", p.returncode)
        print(p.stdout)
        print(p.stderr)
        return {"error": "ffmpeg failed to convert audio"}, 500
    wav_path = "audio.wav"
    # data, samplerate = sf.read(io.BytesIO(audio))

    gp = GaussianParse(wav_path, word, mora_length)
    syllable_clips = gp.splice_audio()

    if len(syllable_clips) == mora_length:
        for i, syllable in enumerate(syllable_clips):
            export_filename = "output/" + word[i] + ".wav"
            # print(export_filename)
            sf.write(export_filename, syllable, 22050)
            # sf_array.append(syllable)
            sf_array.append(export_filename)
    else:
        return jsonify({"error" : "incorrect number of syllables detected."}), 500

    # # gp.plot_waves()
    # for i, syllable in enumerate(syllable_clips):
    #     export_filename = "output/" + word + str(i) + ".wav"
    #     sf.write(export_filename, syllable, 22050)
    #     sf_array.append(syllable)



    result = calculate_grade(wav_path, sf_array, word, word_array, accent_type)

    return jsonify({'grade': result}), 200