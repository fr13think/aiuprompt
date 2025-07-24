from fastapi import APIRouter
from .endpoints import analysis, templates, auth, history

api_router = APIRouter()

api_router.include_router(analysis.router, prefix="/analysis", tags=["Analysis"])
api_router.include_router(templates.router, prefix="/templates", tags=["Templates"])
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(history.router, prefix="/history", tags=["History"])