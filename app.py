from flask import Flask, render_template, request, jsonify, send_file, abort
from logic import convert_files
import os

app = Flask(__name__)

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def upload_files():
    try:
        uploaded_files = request.files.getlist('files')
        imgFormat = request.form.get('imgFormat')
        mode = request.form.get('mode')
        imageSize = int(request.form.get('imageSize'))
        resampling_filter = request.form.get('resampling_filter')
        
        temp_input_dir = 'temp_input'
        if not os.path.exists(temp_input_dir):
            os.makedirs(temp_input_dir)

        uploaded_file_paths = []

        for file in uploaded_files:
            file_path = os.path.join(temp_input_dir, file.filename)
            file.save(file_path)
            uploaded_file_paths.append(file_path)

        zip_filename = convert_files(uploaded_file_paths, imgFormat, mode, imageSize, resampling_filter)
        return jsonify({"zip_filename": zip_filename})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/download', methods=['GET'])
def download_file():
    filename = 'output.zip'
    if filename:
        file_path = os.path.join("zip_output", filename)
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True, download_name=filename)
        else:
            abort(404, "File not found")
    else:
        abort(400, "Invalid request, filename not provided")


if __name__ == "__main__":
    app.run(debug=True)
