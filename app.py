from flask import Flask, render_template, request
from model import load_model, predict_image
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# Load model once
model = load_model()

@app.route('/', methods=['GET', 'POST'])
def index():
    uploaded_image = None
    prediction = None
    confidence = None

    if request.method == 'POST':
        file = request.files.get('file')
        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)  # create folder if not exists
            file.save(file_path)

            # Predict the image
            class_index, confidence = predict_image(model, file_path)
            class_labels = ['Forests', 'Urban Areas', 'Water Bodies'] 
            prediction = class_labels[class_index]
            uploaded_image = file_path

    return render_template('index.html', uploaded_image=uploaded_image, prediction=prediction, confidence=confidence)

# For local testing only
if __name__ == '__main__':
    app.run(debug=True)
