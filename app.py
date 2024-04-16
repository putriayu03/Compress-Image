import os

from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return render_template("index.html")


@app.route('/convert-to-audio', methods=['POST'])
def convert_to_audio():
    if request.method == 'POST':
        f = request.files['video']
        filename = f.filename

        f.save(f"videos/{secure_filename(filename)}")
        os.system(f"ffmpeg -i videos/{secure_filename(filename)} {os.path.splitext(filename)[0]}.mp3")

        return send_file(f"{os.path.splitext(filename)[0]}.mp3", as_attachment=True)


if __name__ == '__main__':
    app.run()
