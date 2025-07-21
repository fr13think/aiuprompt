import google.generativeai as genai
from fastapi import APIRouter, HTTPException, Depends
from ....core.config import settings
from ....schemas.prompt import PromptAnalysisRequest, PromptAnalysisResponse

router = APIRouter()

# Konfigurasi API Key Google
try:
    genai.configure(api_key=settings.GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    # Ini akan mencegah error saat startup jika API key belum diset
    model = None
    print(f"Peringatan: Gagal mengkonfigurasi Google AI. Pastikan GEMINI_API_KEY sudah benar. Error: {e}")


def get_model():
    if not model:
        raise HTTPException(status_code=503, detail="Layanan AI tidak terkonfigurasi. Periksa API Key di server.")
    return model

@router.post("/", response_model=PromptAnalysisResponse)
async def analyze_prompt(
    request: PromptAnalysisRequest,
    ai_model: genai.GenerativeModel = Depends(get_model)
):
    """
    Menerima prompt dari pengguna, menganalisisnya menggunakan AI,
    dan mengembalikan hasil analisis yang terstruktur.
    """
    meta_prompt = f"""
    Anda adalah seorang ahli "Prompt Engineering" kelas dunia dengan nama 'Uprompt AI'.
    Tugas Anda adalah menganalisis prompt yang diberikan oleh pengguna untuk target model AI: '{request.target_model}'.
    Berikan output HANYA dalam format JSON yang valid dan tidak ada teks lain di luar JSON.

    Prompt yang perlu dianalisis:
    ---
    {request.prompt}
    ---

    Lakukan analisis berdasarkan struktur JSON berikut. Berikan evaluasi yang jujur dan saran yang bisa ditindaklanjuti.
    Skor dari 1-10, di mana 1 sangat buruk dan 10 sangat baik.

    {{
      "clarity_score": <skor_kejernihan_int>,
      "specificity_score": <skor_spesifisitas_int>,
      "technique_analysis": {{
        "detected_techniques": ["<nama_teknik_1>", "<nama_teknik_2>"],
        "explanation": "<penjelasan_singkat_teknik_yang_digunakan>"
      }},
      "ambiguity_potential": "<analisis_potensi_ambiguitas_dan_salah_tafsir>",
      "improvement_suggestions": [
        "<saran_perbaikan_1_yang_konkret>",
        "<saran_perbaikan_2_yang_konkret>",
        "<saran_perbaikan_3_yang_konkret>"
      ],
      "optimized_prompt": "<tulis_ulang_prompt_pengguna_menjadi_versi_yang_lebih_baik_berdasarkan_saran_anda>"
    }}
    """
    try:
        response = await ai_model.generate_content_async(meta_prompt)
        
        # Ekstrak konten JSON dari respons AI
        json_text = response.text.strip().replace("```json", "").replace("```", "")
        
        # Parsing string JSON menjadi objek Python
        analysis_data = PromptAnalysisResponse.parse_raw(json_text)
        return analysis_data

    except Exception as e:
        print(f"Error saat berkomunikasi dengan API: {e}")
        # Jika terjadi error, kirim respons error yang informatif
        raise HTTPException(
            status_code=500,
            detail=f"Terjadi kesalahan saat menganalisis prompt. Error: {str(e)}"
        )