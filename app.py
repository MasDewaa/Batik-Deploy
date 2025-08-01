import streamlit as st
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
from PIL import Image
import numpy as np
import io
import os

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

# Load model
@st.cache_resource
def load_my_model():
    model = load_model("mainModel.keras")
    return model

# Load labels
def load_labels(file_path):
    with open(file_path, "r") as f:
        labels = [line.strip() for line in f.readlines()]
    return labels

model = load_my_model()
class_names = load_labels("labels.txt")

# Streamlit UI
st.title("🎨 Batik Classifier")
st.write("Upload gambar batik, lalu lihat prediksinya!")

uploaded_file = st.file_uploader("Pilih file gambar...", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    # Tampilkan gambar
    image = Image.open(uploaded_file)
    st.image(image, caption="Gambar yang diunggah", use_container_width=True)

    # Proses prediksi
    img = image.convert("RGB")
    img = img.resize((160, 160))
    img_array = img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0) / 255.0

    prediction = model.predict(img_array)[0]
    predicted_index = np.argmax(prediction)
    predicted_class = class_names[predicted_index]
    confidence = float(prediction[predicted_index])

    st.write("## ✅ Prediksi:")
    st.write(f"**Motif:** {predicted_class}")
    st.write(f"**Kepercayaan:** {confidence*100:.2f}%")

    st.write("## 🔍 Semua Probabilitas:")
    probs = {class_names[i]: float(prediction[i]) for i in range(len(class_names))}
    sorted_probs = dict(sorted(probs.items(), key=lambda x: x[1], reverse=True))
    st.json(sorted_probs)
