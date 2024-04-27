import os

from flask import Flask, render_template, request, send_file, after_this_request
from werkzeug.utils import secure_filename
from PIL import Image

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return render_template("index.html")


def compress_image(input_path, output_path):
    image = Image.open(input_path)
    width, height = image.size
    new_size = (width // 2, height // 2)
    resized_image = image.resize(new_size)
    resized_image.save(output_path, optimize=True, quality=50)


# Route untuk mengompresi gambar
@app.route('/compress', methods=['POST'])
def compress():
    if request.method == 'POST':
        # Pastikan file gambar diupload dalam request
        if 'image' not in request.files:
            return 'No file part'

        file = request.files['image']

        # Pastikan file memiliki nama dan merupakan file gambar
        if file.filename == '':
            return 'No selected file'

        if file and allowed_file(file.filename):
            # Simpan file yang diupload di server
            filename = secure_filename(file.filename)
            input_path = os.path.join(filename)
            output_path = os.path.join('compressed_' + filename)
            file.save(input_path)

            # Kompresi gambar
            compress_image(input_path, output_path)

            # Setelah kompresi selesai, kirim file yang sudah dicompress sebagai respon
            @after_this_request
            def remove_file(response):
                try:
                    os.remove(input_path)
                    os.remove(output_path)
                except Exception as error:
                    print("Error removing files: ", error)
                return response

            return send_file(output_path, as_attachment=True)


# Fungsi untuk menentukan jenis file yang diizinkan (misalnya, hanya gambar)
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}


if __name__ == '__main__':
    app.run()
