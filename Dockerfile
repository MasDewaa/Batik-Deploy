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

EXPOSE 5000


# ----------------------------
# Gunakan gunicorn sebagai production server
# ----------------------------
CMD ["streamlit", "run", "app.py", "--server.port", "${PORT}", "--server.address", "0.0.0.0"]

