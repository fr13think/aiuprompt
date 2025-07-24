import google.generativeai as genai
import json
from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from google.generativeai.types import GenerationConfigDict

from app import crud, models, schemas
from app.api import deps
from app.core.config import settings

router = APIRouter()

def save_history_task(db: Session, user: models.User, prompt: str, result: schemas.prompt.PromptAnalysisResponse):
    try:
        history_in = schemas.history.HistoryCreate(
            prompt=prompt,
            result=result.model_dump()
        )
        crud.history.create_with_owner(db=db, obj_in=history_in, owner_id=user.id)
        print(f"Histori berhasil disimpan untuk user {user.email}")
    except Exception as e:
        print(f"Error (background task): Gagal menyimpan histori. User: {user.email}. Detail: {e}")

# Konfigurasi API Key Google
try:
    genai.configure(api_key=settings.GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    model = None
    print(f"Peringatan: Gagal mengkonfigurasi Google AI. Pastikan GEMINI_API_KEY sudah benar. Error: {e}")

def get_model():
    if not model:
        raise HTTPException(status_code=503, detail="Layanan AI tidak terkonfigurasi. Periksa API Key di server.")
    return model

@router.post("/", response_model=schemas.prompt.PromptAnalysisResponse)
async def analyze_prompt(
    *,
    background_tasks: BackgroundTasks,
    db: Session = Depends(deps.get_db),
    request: schemas.prompt.PromptAnalysisRequest,
    current_user: models.User | None = Depends(deps.get_current_user_optional),
    ai_model: genai.GenerativeModel = Depends(get_model)
):
    # --- META-PROMPT DALAM BAHASA INDONESIA ---
    meta_prompt = f"""
    Analisis prompt pengguna berikut dan berikan output HANYA dalam format JSON yang valid.
    Objek JSON harus berisi kunci-kunci berikut dengan tipe data yang ditentukan:
    - "clarity_score": integer antara 1 dan 10.
    - "specificity_score": integer antara 1 dan 10.
    - "technique_analysis": objek JSON dengan dua kunci: "detected_techniques" (sebuah list of strings) dan "explanation" (sebuah string).
    - "ambiguity_potential": sebuah string yang menganalisis potensi ambiguitas.
    - "improvement_suggestions": sebuah list of strings dengan saran-saran perbaikan yang konkret.
    - "optimized_prompt": sebuah string berisi versi prompt pengguna yang sudah ditingkatkan.
    Semua respons teks harus dalam Bahasa Indonesia.

    Prompt pengguna yang akan dianalisis: "{request.prompt}"
    """
    try:
        generation_config = GenerationConfigDict(response_mime_type="application/json")
        response = await ai_model.generate_content_async(
            meta_prompt,
            generation_config=generation_config
        )
        
        analysis_data = schemas.prompt.PromptAnalysisResponse.model_validate_json(response.text)

        if current_user:
            background_tasks.add_task(
                save_history_task, db, current_user, request.prompt, analysis_data
            )

        return analysis_data

    except Exception as e:
        print(f"Error saat berkomunikasi dengan API atau memvalidasi data: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Terjadi kesalahan saat menganalisis prompt. Error: {str(e)}"
        )