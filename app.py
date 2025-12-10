from flask import Flask, render_template, request, send_from_directory
import os
import uuid
from HD_RL_Tracker import process_text

app = Flask(__name__)

# Upload folder for the text file
app.config['UPLOAD_FOLDER'] = './uploads'
app.config['CSV_FOLDER'] = './static/csv'

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['CSV_FOLDER'], exist_ok=True)

# Home route to show the upload form
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle the file upload
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part', 400
    
    file = request.files['file']
    
    if file.filename == '':
        return 'No selected file', 400

    # Save the uploaded file to a unique filename
    filename = f"{uuid.uuid4().hex}.txt"
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    # Process the text file and convert it to CSV
    csv_filename = process_text(file_path, app.config['CSV_FOLDER'])

    # Return the CSV file for download
    return send_from_directory(app.config['CSV_FOLDER'], csv_filename)

if __name__ == '__main__':
    app.run(debug=True)
