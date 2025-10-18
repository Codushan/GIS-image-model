# app.py

from flask import Flask, render_template, request
from model import load_model, predict_image
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# Load model
model = load_model()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            # Predict the image
            class_index, confidence = predict_image(model, file_path)
            class_labels = ['Forests', 'Urban Areas', 'Water Bodies'] 
            prediction = class_labels[class_index]

            return render_template('index.html', uploaded_image=file_path, prediction=prediction, confidence=confidence)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
