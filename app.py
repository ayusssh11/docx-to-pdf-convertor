from flask import Flask, render_template, request, send_from_directory
from docx2pdf import convert
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'

# Ensure upload and output directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert_docx_to_pdf():
    if 'docx_file' not in request.files:
        return "No file part", 400

    file = request.files['docx_file']
    
    if file.filename == '':
        return "No selected file", 400

    # Save the uploaded file
    input_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(input_path)

    # Convert DOCX to PDF
    output_path = os.path.join(OUTPUT_FOLDER, f"{os.path.splitext(file.filename)[0]}.pdf")
    convert(input_path, output_path)

    return send_from_directory(OUTPUT_FOLDER, os.path.basename(output_path), as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
