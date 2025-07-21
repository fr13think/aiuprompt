from fastapi import APIRouter
from typing import List, Dict

router = APIRouter()

PROMPT_TEMPLATES: List[Dict[str, str]] = [
    {
        "title": "Membuat Deskripsi Produk",
        "prompt": "Bertindaklah sebagai copywriter profesional. Buat deskripsi produk yang menarik dan menjual untuk [NAMA PRODUK]. Target audiensnya adalah [TARGET AUDIENS]. Sebutkan keunggulan utamanya: [KEUNGGULAN 1], [KEUNGGULAN 2], dan [KEUNGGULAN 3]. Gunakan gaya bahasa yang [GAYA BAHASA, misal: santai dan humoris]."
    },
    {
        "title": "Brainstorming Ide Konten",
        "prompt": "Berikan saya 5 ide konten YouTube yang unik seputar topik [TOPIK UTAMA]. Untuk setiap ide, sertakan judul yang menarik dan satu paragraf singkat tentang isi videonya."
    },
    {
        "title": "Menulis Email Pemasaran",
        "prompt": "Tulis sebuah draf email pemasaran untuk mengumumkan peluncuran [PRODUK/FITUR BARU]. Tujuan email ini adalah untuk mendorong pengguna agar [TUJUAN AKSI, misal: mencoba fitur baru, melakukan pembelian]. Subjek email harus singkat dan menarik perhatian."
    }
]

@router.get("/", response_model=List[Dict[str, str]])
def get_prompt_templates():
    """Mengembalikan daftar template prompt yang sudah disiapkan."""
    return PROMPT_TEMPLATES