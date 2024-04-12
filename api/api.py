import time
import subprocess
from base64 import b64decode
from flask import Flask, request, jsonify
from gaussian_parse import GaussianParse
import soundfile as sf
import io

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
    gp.plot_waves()
    for i, syllable in enumerate(syllable_clips):
        export_filename = "output/" + "仕事" + str(i) + ".wav"
        sf.write(export_filename, syllable, 22050)

    return jsonify("it works"), 200