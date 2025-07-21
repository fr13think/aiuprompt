# uprompt-ai

**uprompt-ai** adalah sebuah alat analisis dan optimisasi prompt berbasis AI yang cerdas. Aplikasi ini membantu pengguna untuk menyempurnakan instruksi mereka kepada model bahasa (LLM) untuk mendapatkan hasil yang lebih akurat, relevan, dan berkualitas tinggi.

Dibangun dengan tumpukan teknologi modern, uprompt-ai dirancang untuk menjadi cepat, efisien, dan mudah digunakan.

---

### ## Fitur Utama (MVP)

* **Analisis Prompt Fundamental**: Memberikan skor dan evaluasi mendalam terhadap kejelasan, spesifisitas, dan potensi ambiguitas sebuah prompt.
* **Saran Perbaikan**: Memberikan rekomendasi konkret untuk meningkatkan kualitas prompt.
* **Desain Intuitif**: Antarmuka yang bersih dan modern dengan tema gelap untuk kenyamanan penggunaan.
* **Cepat & Responsif**: Dibangun dengan FastAPI di backend dan vanilla JavaScript di frontend untuk kecepatan maksimal.

---

### ## Tumpukan Teknologi

* **Backend**: Python, FastAPI
* **Frontend**: HTML, CSS, JavaScript
* **AI Core**: Google Gemini API
* **Deployment**: Docker, Render

---

### ## Menjalankan Secara Lokal

1.  **Prasyarat**:
    * Docker Desktop terinstal dan berjalan.
    * Git

2.  **Clone Repository**:
    ```bash
    git clone [URL_REPOSITORY_ANDA]
    cd uprompt-ai
    ```

3.  **Setup Environment Variable**:
    * Buat file bernama `.env` di dalam folder `backend/`.
    * Salin isi dari `backend/.env.example` dan masukkan API Key Anda.
        ```
        GEMINI_API_KEY="AIzaSy...ANDA"
        ```

4.  **Build dan Jalankan dengan Docker**:
    ```bash
    docker build -t uprompt-ai .
    docker run -p 8000:8000 uprompt-ai
    docker-compose down
    docker-compose up --build
    docker-compose build backend
    docker-compose run --rm backend python -m alembic init alembic
    docker-compose run --rm backend python -m alembic revision --autogenerate -m "Create initial tables"
    docker-compose run --rm backend python -m alembic upgrade head
    docker-compose logs backend
    docker-compose down
    docker-compose up -d
    ```

5.  **Akses Aplikasi**:
    * Buka browser Anda dan navigasikan ke `http://localhost:8000`

https://djecrety.ir/