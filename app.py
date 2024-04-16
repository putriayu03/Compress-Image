import os

from flask import Flask, render_template, request, send_file, after_this_request
from werkzeug.utils import secure_filename

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return render_template("index.html")


@app.route('/convert-to-audio', methods=['POST'])
def convert_to_audio():
    if request.method == 'POST':
        f = request.files['video']
        filename = secure_filename(f.filename)
        f.save(f"{filename}")
        os.system(f"ffmpeg -i {filename} {os.path.splitext(filename)[0]}.mp3")

        os.remove(f"{filename}")

        @after_this_request
        def remove_video (response) :
            try:
                os.remove(f"{os.path.splitext(filename)[0]}.mp3")
            except Exception as e :
                print("Gagal menghapus video!")
            return response

        return send_file(f"{os.path.splitext(filename)[0]}.mp3", as_attachment=True)


if __name__ == '__main__':
    app.run()
