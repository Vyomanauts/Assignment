import os
import sys
from flask import Flask, request, render_template, jsonify

# Ensure Python finds the pitch_analyzer module
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

import pitch_analyzer  # Now Python should recognize it

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"  # Keep the uploads inside assignment2
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)
    
    # Call the pitch analysis function
    analysis_results = pitch_analyzer.analyze_pitch(file_path)
    
    return jsonify({'results': analysis_results})

if __name__ == '__main__':
    app.run(debug=True)
