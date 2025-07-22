from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Any

from app import crud, schemas
from app.api import deps
from app.core.security import create_access_token, verify_password # Tambah import verify_password

router = APIRouter()

@router.post("/register", response_model=schemas.user.User)
def register_user(
    *,
    db: Session = Depends(deps.get_db),
    user_in: schemas.user.UserCreate,
) -> Any:
    """
    Buat user baru.
    """
    user = crud.user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="User dengan email ini sudah ada di dalam database.",
        )
    user = crud.user.create(db, obj_in=user_in)
    return user

@router.post("/login", response_model=schemas.token.Token)
def login_for_access_token(
    db: Session = Depends(deps.get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    Login untuk mendapatkan access token.
    """
    user = crud.user.get_by_email(db, email=form_data.username)
    if not user or not user.is_active:
        raise HTTPException(status_code=400, detail="Email atau password salah")

    # PERBAIKAN ADA DI SINI: Panggil 'verify_password' langsung
    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Email atau password salah")
    
    access_token = create_access_token(
        subject=user.email,
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
    }