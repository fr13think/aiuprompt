# Fase 1: Build Backend
FROM python:3.11-slim AS backend-builder

WORKDIR /app

# Instal dependensi Python
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Salin kode backend
COPY backend/ .

# Fase 2: Final Image
# Gunakan image yang sama untuk menjaga konsistensi
FROM python:3.11-slim

WORKDIR /app

# Salin dependensi yang sudah terinstal dari fase builder
COPY --from=backend-builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages

# Salin kode aplikasi dari fase builder
COPY --from=backend-builder /app /app

# Salin kode frontend
COPY frontend/ /app/frontend/

# Ekspos port yang akan digunakan oleh Uvicorn
EXPOSE 8000

# Perintah untuk menjalankan aplikasi
# Uvicorn akan menjalankan aplikasi FastAPI di 'main.py' dan juga menyajikan file statis dari folder 'frontend'
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]