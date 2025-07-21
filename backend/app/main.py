from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from .api.v1 import api as api_v1

# Inisialisasi aplikasi FastAPI
app = FastAPI(
    title="uprompt-ai API",
    description="API untuk menganalisis dan mengoptimalkan prompt AI.",
    version="1.0.0"
)

# Pengaturan CORS (Cross-Origin Resource Sharing)
# Ini memungkinkan frontend (yang berjalan di domain berbeda) untuk berkomunikasi dengan backend
origins = [
    "http://localhost",
    "http://localhost:8000",
    # Tambahkan domain production Anda di sini nanti
    "https://aiu-prompt.onrender.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Sertakan router API dari versi v1
app.include_router(api_v1.api_router, prefix="/api/v1")

# Menyajikan file statis (frontend)
# Ini membuat FastAPI juga berfungsi sebagai web server untuk file HTML, CSS, JS Anda
# __file__ adalah file main.py ini. Path(...).resolve().parent.parent adalah folder 'backend'
# Jadi, path ke folder frontend adalah 'backend/../frontend' -> 'frontend'
frontend_dir = Path(__file__).resolve().parent.parent / 'frontend'

app.mount("/", StaticFiles(directory=str(frontend_dir), html=True), name="static")


@app.get("/health", tags=["Status"])
def health_check():
    """Endpoint sederhana untuk memeriksa apakah server berjalan."""
    return {"status": "ok"}