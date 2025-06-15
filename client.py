import requests
import os
import sys

# -----------------------------
# ✅ Konfigurasi
# -----------------------------
API_URL = "https://batik-deploy.railway.app/predict"

# Ganti path ini sesuai file gambar lokalmu
IMAGE_PATH = "../Batik Nitik Grouped/Brendhi/11 Brendhi 1_rotate_90.jpg"

# -----------------------------
# 🚀 Fungsi utama
# -----------------------------

def main():
    # Cek file
    if not os.path.exists(IMAGE_PATH):
        print(f"[ERROR] File tidak ditemukan: {IMAGE_PATH}")
        sys.exit(1)

    # Siapkan multipart form-data
    with open(IMAGE_PATH, "rb") as f:
        files = {"file": (os.path.basename(IMAGE_PATH), f)}
        try:
            print(f"[INFO] Mengirim gambar ke: {API_URL}")
            response = requests.post(API_URL, files=files)

            # Debug status
            print(f"[INFO] Status code: {response.status_code}")

            if response.status_code == 200:
                data = response.json()
                print("\n=== ✅ Prediksi Berhasil ===")
                print(f"  Motif Terdeteksi     : {data['data']['class_name']}")
                print(f"  Confidence (angka)   : {data['data']['confidence']}")
                print(f"  Confidence (percent) : {data['data']['confidence_percent']}")
                print(f"  Top 5 Probabilities  :")
                for k, v in data['data']['probabilities'].items():
                    print(f"    - {k}: {v:.4f}")
            else:
                print("\n=== ❌ Gagal Prediksi ===")
                try:
                    print(response.json())
                except Exception:
                    print(response.text)

        except requests.exceptions.RequestException as e:
            print(f"[ERROR] Tidak dapat terhubung ke API: {e}")


# -----------------------------
# ▶️  Run script
# -----------------------------
if __name__ == "__main__":
    main()
