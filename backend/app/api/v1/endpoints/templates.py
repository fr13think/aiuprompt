from fastapi import APIRouter
from typing import List, Dict

router = APIRouter()

PROMPT_TEMPLATES: List[Dict[str, str]] = [
    # --- Template yang sudah ada ---
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
    },
    {
        "title": "Menulis Narasi Berita",
        "prompt": "Anda adalah seorang jurnalis. Tulis sebuah narasi berita yang informatif dan objektif berdasarkan informasi berikut:\n\n- Judul Utama: [JUDUL UTAMA BERITA]\n- 5 Poin Kunci Peristiwa: [POIN 1, POIN 2, POIN 3, ...]\n- Narasumber (jika ada): [NAMA NARASUMBER DAN KUTIPANNYA]\n\nGunakan gaya bahasa jurnalistik yang lugas dan пирамида terbalik."
    },
    {
        "title": "Membuat Notulen Rapat (Meeting)",
        "prompt": "Buat notulen rapat (Minutes of Meeting) yang ringkas dan profesional dari poin-poin berikut:\n\n- Topik Rapat: [TOPIK UTAMA RAPAT]\n- Tanggal & Waktu: [TANGGAL & WAKTU]\n- Daftar Peserta: [NAMA PESERTA 1, 2, 3, ...]\n- Poin Diskusi Utama & Keputusan: [MASUKKAN POIN-POIN DISKUSI ATAU TRANSKRIP MENTAH DI SINI]\n\nFormat hasilnya dalam bentuk poin-poin yang jelas, termasuk action items (beserta penanggung jawabnya) dan tenggat waktu."
    },
    {
        "title": "Menyusun Laporan Pekerjaan",
        "prompt": "Buat draf laporan pekerjaan [HARIAN/MINGGUAN/BULANAN] yang profesional untuk periode [PERIODE LAPORAN]. Laporan harus mencakup bagian-bagian berikut:\n\n1.  Tugas yang Telah Selesai: [DAFTAR TUGAS YANG SUDAH SELESAI]\n2.  Tugas yang Sedang Berjalan: [DAFTAR TUGAS YANG SEDANG DIKERJAKAN]\n3.  Tantangan atau Hambatan: [JELASKAN TANTANGAN YANG DIHADAPI]\n4.  Rencana untuk Periode Berikutnya: [DAFTAR RENCANA KERJA]\n\nPastikan bahasa yang digunakan formal dan jelas."
    }
]

@router.get("/", response_model=List[Dict[str, str]])
def get_prompt_templates():
    """Mengembalikan daftar template prompt yang sudah disiapkan."""
    return PROMPT_TEMPLATES