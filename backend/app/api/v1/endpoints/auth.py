from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Any

from app import crud  # <-- Impor 'crud' sebagai package
from app.schemas import user as user_schema, token as token_schema
from app.api import deps
from app.core.security import create_access_token

router = APIRouter()

@router.post("/register", response_model=user_schema.User)
def register_user(
    *,
    db: Session = Depends(deps.get_db),
    user_in: user_schema.UserCreate,
) -> Any:
    """
    Buat user baru.
    """
    # Panggil fungsi melalui crud.user (sesuai nama instance di crud_user.py)
    user = crud.user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="User dengan email ini sudah ada.",
        )
    user = crud.user.create(db, obj_in=user_in)
    return user

@router.post("/login", response_model=token_schema.Token)
def login_for_access_token(
    db: Session = Depends(deps.get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    Login untuk mendapatkan access token.
    """
    # Panggil fungsi melalui crud.user
    user = crud.user.get_by_email(db, email=form_data.username)
    if not user or not user.is_active:
        raise HTTPException(status_code=400, detail="Email atau password salah")

    # Panggil fungsi melalui crud.user
    if not crud.user.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Email atau password salah")
    
    access_token = create_access_token(
        subject=user.email,
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
    }