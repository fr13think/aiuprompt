from sqlalchemy.orm import Session
from .base import CRUDBase
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import get_password_hash, verify_password as verify_pwd

class CRUDUser(CRUDBase[User, UserCreate]):
    def get_by_email(self, db: Session, *, email: str) -> User:
        return db.query(User).filter(User.email == email).first()

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        db_obj = User(
            email=obj_in.email,
            hashed_password=get_password_hash(obj_in.password),
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    # Perbaikan ada di sini, kita memanggil 'verify_pwd' yang sudah diimpor
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return verify_pwd(plain_password, hashed_password)

user = CRUDUser(User)