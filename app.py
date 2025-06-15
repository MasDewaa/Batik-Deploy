from flask import Flask, request, jsonify
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
from PIL import Image
import numpy as np
import os
import io

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

app = Flask(__name__)

# --- FUNGSI UNTUK MEMUAT LABELS DARI FILE ---
def load_labels(file_path):
    """Membaca file label dan mengembalikannya sebagai list."""
    try:
        with open(file_path, 'r') as f:
            # Menggunakan list comprehension untuk membaca setiap baris dan menghapus karakter newline (\n)
            labels = [line.strip() for line in f.readlines()]
        print(f">>> Berhasil memuat {len(labels)} label dari {file_path}")
        return labels
    except FileNotFoundError:
        print(f"!!! FATAL ERROR: File label '{file_path}' tidak ditemukan.")
        print("!!! Aplikasi tidak dapat berjalan tanpa file label. Harap buat file labels.txt.")
        # Menghentikan program jika file label tidak ada, karena API tidak akan berguna.
        exit()

# --- PENGATURAN DAN PEMUATAN MODEL & LABELS ---
try:
    model = load_model("final_tuned_model.keras")
    print(">>> Model berhasil dimuat.")
except Exception as e:
    print(f"!!! Error saat memuat model: {e}")
    model = None

# Memuat nama kelas dari file labels.txt
class_names = load_labels("labels.txt")

# --- FUNGSI PREPROCESSING GAMBAR (Tetap sama) ---
def preprocess_image(pil_image, target_size=(224, 224)):
    if pil_image.mode != "RGB":
        pil_image = pil_image.convert("RGB")
    pil_image = pil_image.resize(target_size)
    img_array = img_to_array(pil_image)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array / 255.0
    return img_array

# --- DEFINISI ENDPOINT API (Tetap sama) ---
@app.route("/api/v1", methods=["GET"])
def index():
    return jsonify({
        "status": "online",
        "message": "API Klasifikasi Motif Batik Siap Digunakan. Gunakan endpoint /api/predict untuk prediksi."
    })

@app.route("/api/v1/predict", methods=["POST"])
def predict():
    if model is None:
        return jsonify({"error": "Model tidak tersedia, periksa log server."}), 500

    if 'file' not in request.files:
        return jsonify({"error": "Tidak ada file yang dikirim. Gunakan key 'file'."}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "File yang dikirim tidak memiliki nama."}), 400

    try:
        image_bytes = file.read()
        pil_image = Image.open(io.BytesIO(image_bytes))
        processed_image = preprocess_image(pil_image)
        
        # 1. Lakukan prediksi, hasilnya adalah array probabilitas
        prediction_array = model.predict(processed_image)[0] # Ambil array pertama dari batch

        # 2. Dapatkan kelas dengan probabilitas tertinggi
        predicted_index = np.argmax(prediction_array)
        predicted_class = class_names[predicted_index]
        confidence = float(prediction_array[predicted_index])

        # 3. Buat dictionary untuk semua probabilitas {nama_kelas: probabilitas}
        # Menggunakan zip untuk menggabungkan nama kelas dengan probabilitasnya
        all_probabilities = {class_names[i]: float(prediction_array[i]) for i in range(len(class_names))}
        
        # (Opsional) Jika Anda hanya ingin beberapa probabilitas teratas (misal 5 teratas)
        sorted_probabilities = sorted(all_probabilities.items(), key=lambda item: item[1], reverse=True)
        top_5_probabilities = dict(sorted_probabilities[:5])

        # 4. Bangun format JSON yang diinginkan
        return jsonify({
            "success": True,
            "data": {
                "class_name": predicted_class,
                "confidence": confidence,
                "confidence_percent": f"{confidence * 100:.2f}%",
                "probabilities": top_5_probabilities # atau gunakan top_5_probabilities jika Anda memilih opsi di atas
            }
        })


    except Exception as e:
        return jsonify({
            "status": False,
            "message": "Terjadi kesalahan saat memproses gambar. Pastikan file adalah format gambar yang valid.",
            "error_details": str(e)
        }), 400

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)