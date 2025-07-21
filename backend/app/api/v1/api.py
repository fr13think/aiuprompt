from fastapi import APIRouter
from .endpoints import analysis, templates, auth

api_router = APIRouter()

# Sertakan router dari 'analysis.py'
api_router.include_router(analysis.router, prefix="/analysis", tags=["Analysis"])

# Sertakan router dari 'templates.py'
api_router.include_router(templates.router, prefix="/templates", tags=["Templates"])

api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])

