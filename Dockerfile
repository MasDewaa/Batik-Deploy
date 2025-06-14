# Tahap 1: Pilih base image yang ringan dan sudah terinstall Python
FROM python:3.9-slim

# Tahap 2: Atur direktori kerja di dalam container
WORKDIR /app

# Tahap 3: Salin file requirements terlebih dahulu
# (Ini memanfaatkan cache Docker, jika requirements tidak berubah, langkah ini tidak diulang)
COPY requirements.txt .

# Tahap 4: Install semua dependensi Python
RUN pip install --no-cache-dir -r requirements.txt

# Tahap 5: Salin sisa kode aplikasi dan model ke dalam direktori kerja (/app)
COPY . .

# Tahap 6: Beri tahu Docker bahwa container akan listen di port 5000
EXPOSE 5000

# Tahap 7: Perintah yang akan dijalankan saat container启动
# Kita menggunakan Gunicorn untuk menjalankan aplikasi Flask kita
# api_server:app  => jalankan variabel 'app' dari file 'api_server.py'
# --workers 2     => jumlah proses worker (sesuaikan dengan CPU server Anda)
# --threads 4     => jumlah thread per worker
# --bind 0.0.0.0:5000 => listen di semua network interface pada port 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]