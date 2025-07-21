from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..core.config import settings

engine = create_engine(settings.DATABASE_URL)

# Buat SessionLocal class yang akan kita gunakan untuk setiap sesi database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)