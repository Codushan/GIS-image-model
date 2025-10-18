import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image
from model import load_model, predict_image
import os

# Page config
st.set_page_config(
    page_title="GIS Image Classification",
    page_icon="🌍",
    layout="centered"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .stButton>button {
        width: 100%;
        background-color: #28a745;
        color: white;
        font-size: 18px;
        padding: 10px;
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.title("🌍 GIS Image Classification")
st.markdown("### Upload satellite/aerial images to classify land cover")

# Load model with caching
@st.cache_resource
def get_model():
    return load_model()

model = get_model()

# File uploader
uploaded_file = st.file_uploader(
    "Choose an image...", 
    type=['jpg', 'jpeg', 'png'],
    help="Upload satellite or aerial imagery"
)

if uploaded_file is not None:
    # Display image
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_container_width =True)
    
    # Create temporary file
    temp_path = "temp_image.jpg"
    image.save(temp_path)
    
    # Predict button
    if st.button('🔍 Classify Image'):
        with st.spinner('Analyzing image...'):
            try:
                # Predict
                class_index, confidence = predict_image(model, temp_path)
                
                # Class labels
                class_labels = ['Forests', 'Urban Areas', 'Water Bodies']
                prediction = class_labels[class_index]
                
                # Display results
                st.success("Classification Complete!")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric(label="Prediction", value=prediction)
                with col2:
                    st.metric(label="Confidence", value=f"{confidence*100:.2f}%")
                
                # Progress bar for confidence
                st.progress(float(confidence))
                
            except Exception as e:
                st.error(f"Error: {str(e)}")
            finally:
                # Clean up
                if os.path.exists(temp_path):
                    os.remove(temp_path)

# Sidebar info
with st.sidebar:
    st.header("ℹ️ About")
    st.info("""
    This app classifies satellite/aerial images into:
    - 🌲 Forests
    - 🏙️ Urban Areas
    - 💧 Water Bodies
    
    Upload an image to get started!
    """)
    
    st.header("📊 Model Info")
    st.write("Image Size: 150x150")
    st.write("Classes: 3")