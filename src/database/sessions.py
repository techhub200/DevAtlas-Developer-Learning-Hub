from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine

from src.core.config import DATABASE_URL

engine = create_engine(DATABASE_URL)

# bind the session to the engine (fixes UnboundExecutionError)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# create a dependency injection
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

