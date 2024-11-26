from flask import Flask, render_template, request, send_file
import os
import subprocess

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
WOFF2_TOOL_PATH = "./woff2/woff2_decompress"  # Path to your woff2_decompress executable

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/convert', methods=['POST'])
def convert():
    if 'file' not in request.files:
        return "No file uploaded", 400

    uploaded_file = request.files['file']
    if uploaded_file.filename == '':
        return "No selected file", 400

    if not uploaded_file.filename.endswith('.woff2'):
        return "Please upload a valid WOFF2 file", 400

    # Save the uploaded WOFF2 file
    input_path = os.path.join(UPLOAD_FOLDER, uploaded_file.filename)
    uploaded_file.save(input_path)

    # Convert the WOFF2 file to TTF
    try:
        subprocess.run([WOFF2_TOOL_PATH, input_path], check=True)
        ttf_path = input_path.replace(".woff2", ".ttf")  # The output TTF file
    except subprocess.CalledProcessError:
        return "Conversion failed", 500

    return send_file(ttf_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)