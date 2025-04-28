from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
import os
DATABASE_URL = "sqlite:///Database/database.db"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()

# Singleton-like access
class DBSession:
    _session: Session = None

    @classmethod
    def get(cls) -> Session:
        if cls._session is None:
            cls._session = SessionLocal()
        return cls._session

    @classmethod
    def close(cls):
        if cls._session:
            cls._session.close()
            cls._session = None