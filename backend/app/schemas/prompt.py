from pydantic import BaseModel, Field
from typing import List

class PromptAnalysisRequest(BaseModel):
    prompt: str = Field(..., min_length=10, description="Prompt yang akan dianalisis oleh AI.")
    target_model: str = "default" 

class TechniqueAnalysis(BaseModel):
    detected_techniques: List[str]
    explanation: str

class PromptAnalysisResponse(BaseModel):
    clarity_score: int = Field(..., ge=1, le=10)
    specificity_score: int = Field(..., ge=1, le=10)
    technique_analysis: TechniqueAnalysis
    ambiguity_potential: str
    improvement_suggestions: List[str]
    optimized_prompt: str