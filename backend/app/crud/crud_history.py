from sqlalchemy.orm import Session
from .base import CRUDBase
from app.models.history import AnalysisHistory
from app.schemas.history import HistoryCreate

class CRUDHistory(CRUDBase[AnalysisHistory, HistoryCreate]):
    def create_with_owner(
        self, db: Session, *, obj_in: HistoryCreate, owner_id: int
    ) -> AnalysisHistory:
        # Konversi Pydantic model ke dictionary
        obj_in_data = obj_in.model_dump()
        db_obj = self.model(**obj_in_data, owner_id=owner_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_owner(
        self, db: Session, *, owner_id: int, skip: int = 0, limit: int = 100
    ) -> list[AnalysisHistory]:
        return (
            db.query(self.model)
            .filter(AnalysisHistory.owner_id == owner_id)
            .order_by(AnalysisHistory.created_at.desc()) # Urutkan dari yang terbaru
            .offset(skip)
            .limit(limit)
            .all()
        )

history = CRUDHistory(AnalysisHistory)