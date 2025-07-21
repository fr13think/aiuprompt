from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from ..db.base_class import Base

class AnalysisHistory(Base):
    id = Column(Integer, primary_key=True, index=True)
    prompt = Column(String, nullable=False)
    result = Column(JSON, nullable=False)
    owner_id = Column(Integer, ForeignKey("user.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

    owner = relationship("User")