from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app import crud, models, schemas
from app.api import deps

router = APIRouter()

@router.post("/", response_model=schemas.history.History)
def create_history(
    *,
    db: Session = Depends(deps.get_db),
    history_in: schemas.history.HistoryCreate,
    current_user: models.User = Depends(deps.get_current_user),
):
    """
    Buat entri histori analisis baru untuk pengguna yang sedang login.
    """
    history = crud.history.create_with_owner(
        db=db, obj_in=history_in, owner_id=current_user.id
    )
    return history

@router.get("/", response_model=List[schemas.history.History])
def read_history(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_user),
):
    """
    Ambil daftar histori analisis milik pengguna yang sedang login.
    """
    history = crud.history.get_multi_by_owner(
        db, owner_id=current_user.id, skip=skip, limit=limit
    )
    return history