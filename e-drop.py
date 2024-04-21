from flask import Flask, render_template, request, jsonify, send_from_directory, send_file
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

uploaded_files = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    filename = file.filename
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    uploaded_files[filename] = file_path

    return jsonify({'message': 'File uploaded successfully', 'filename': filename}), 200

@app.route('/filelist')
def file_list():
    return jsonify(list(uploaded_files.keys()))

@app.route('/download/<filename>')
def download_file(filename):
    if filename in uploaded_files:
        file_path = uploaded_files[filename]
        return send_file(file_path, as_attachment=True)
    else:
        return jsonify({'error': 'File not found'}), 404

@app.route('/stream/<filename>')
def stream_file(filename):
    if filename in uploaded_files:
        file_path = uploaded_files[filename]
        return send_file(file_path)
    else:
        return jsonify({'error': 'File not found'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
