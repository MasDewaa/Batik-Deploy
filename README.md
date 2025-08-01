# 🎨 Batik Classifier

Aplikasi machine learning untuk mengklasifikasikan motif batik menggunakan TensorFlow dan Streamlit.

## 🌐 Live Demo
https://masdewaa-batik-deploy-app-djhprv.streamlit.app/

## 🚀 Cara Deploy ke Streamlit Cloud

### Langkah 1: Siapkan Repository
1. Pastikan semua file sudah ada di repository GitHub:
   - `app.py` - File utama aplikasi
   - `requirements.txt` - Dependencies
   - `final_tuned_model.keras` - Model TensorFlow
   - `labels.txt` - Label klasifikasi
   - `.streamlit/config.toml` - Konfigurasi Streamlit

### Langkah 2: Deploy ke Streamlit Cloud
1. Buka [share.streamlit.io](https://share.streamlit.io)
2. Login dengan akun GitHub
3. Klik "New app"
4. Pilih repository dan branch
5. Set main file path: `app.py`
6. Klik "Deploy!"

### Langkah 3: Konfigurasi (Opsional)
- **Memory**: Jika model besar, set memory limit di Streamlit Cloud
- **Timeout**: Sesuaikan timeout untuk model inference

## 📁 Struktur File
```
Batik-Deploy/
├── app.py                 # Aplikasi utama
├── requirements.txt       # Dependencies
├── final_tuned_model.keras # Model TensorFlow
├── labels.txt            # Label klasifikasi
├── .streamlit/
│   └── config.toml      # Konfigurasi Streamlit
└── README.md            # Dokumentasi
```

## 🔧 Cara Menjalankan Lokal

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Jalankan aplikasi:
```bash
streamlit run app.py
```

## 🐛 Troubleshooting

### Error "dense_2 expects 1 input but received 2"
- Pastikan model sudah di-compile dengan benar
- Coba load model dengan `compile=False`
- Periksa arsitektur model

### Memory Issues
- Gunakan model yang lebih kecil
- Optimasi preprocessing gambar
- Set memory limit di Streamlit Cloud

## 📝 Fitur
- ✅ Upload gambar batik
- ✅ Klasifikasi motif otomatis
- ✅ Tampilkan confidence score
- ✅ Responsive UI
- ✅ Error handling

## 🤝 Kontribusi
Silakan buat pull request untuk perbaikan atau fitur baru!
