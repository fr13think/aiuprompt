from sqlalchemy.orm import Session
from .base import CRUDBase
from app.models.history import AnalysisHistory
from app.schemas.history import HistoryCreate

class CRUDHistory(CRUDBase[AnalysisHistory, HistoryCreate]):
    def get_multi_by_owner(
        self, db: Session, *, owner_id: int, skip: int = 0, limit: int = 100
    ) -> list[AnalysisHistory]:
        return (
            db.query(self.model)
            .filter(AnalysisHistory.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

history = CRUDHistory(AnalysisHistory)