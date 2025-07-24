from pydantic import BaseModel, Json
from datetime import datetime

# Skema dasar untuk data analisis yang disimpan
class AnalysisResult(BaseModel):
    clarity_score: int
    specificity_score: int
    technique_analysis: dict
    ambiguity_potential: str
    improvement_suggestions: list[str]
    optimized_prompt: str

# Skema untuk membuat entri histori baru
class HistoryCreate(BaseModel):
    prompt: str
    result: AnalysisResult

# Skema untuk menampilkan entri histori dari database
class History(HistoryCreate):
    id: int
    owner_id: int
    created_at: datetime

    class Config:
        from_attributes = True