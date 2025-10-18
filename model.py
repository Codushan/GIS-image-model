# model.py

import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing.image import load_img, img_to_array

# Load the model
def load_model():
    model = tf.keras.models.load_model('data/model/model.h5')
    return model

# Predict class of an image
def predict_image(model, image_path, img_width=150, img_height=150):
    image = load_img(image_path, target_size=(img_width, img_height))
    image_array = img_to_array(image) / 255.0
    image_array = np.expand_dims(image_array, axis=0)
    predictions = model.predict(image_array)
    class_index = np.argmax(predictions, axis=1)[0]
    confidence = np.max(predictions, axis=1)[0]
    return class_index, confidence
