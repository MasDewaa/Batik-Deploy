# ----------------------------
# Gunakan Python base image
# ----------------------------
FROM python:3.10-slim

# ----------------------------
# Atur working directory
# ----------------------------
WORKDIR /app

# ----------------------------
# Copy requirements
# ----------------------------
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# ----------------------------
# Copy semua file project ke container
# ----------------------------
COPY . .

# ----------------------------
# Gunakan gunicorn sebagai production server
# ----------------------------
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
