import requests
import os

# URL endpoint API
API_URL = "https://batik-deploy.railway.app/predict"

# Path ke gambar yang ingin diprediksi
IMAGE_PATH = "../Batik Nitik Grouped/Brendhi/11 Brendhi 1_rotate_90.jpg" # <-- GANTI INI

# Cek apakah file ada
if not os.path.exists(IMAGE_PATH):
    print(f"Error: File tidak ditemukan di {IMAGE_PATH}")
else:
    # Buka file gambar dalam mode binary read ('rb')
    with open(IMAGE_PATH, 'rb') as image_file:
        # Siapkan file untuk dikirim dalam permintaan multipart/form-data
        files = {'file': (os.path.basename(IMAGE_PATH), image_file)}

        try:
            # Kirim permintaan POST ke API
            response = requests.post(API_URL, files=files)

            # Cek apakah permintaan berhasil (status code 200 OK)
            if response.status_code == 200:
                # Tampilkan hasil prediksi dari respons JSON
                result = response.json()
                print("Prediksi Berhasil!")
                print(f"  Motif: {result['prediction']}")
                print(f"  Tingkat Kepercayaan: {result['confidence_percent']}")
            else:
                # Tampilkan pesan error jika permintaan gagal
                print(f"Error: Gagal melakukan prediksi (Status Code: {response.status_code})")
                print("Respons dari server:")
                print(response.json())

        except requests.exceptions.RequestException as e:
            print(f"Error: Tidak dapat terhubung ke server API. {e}")