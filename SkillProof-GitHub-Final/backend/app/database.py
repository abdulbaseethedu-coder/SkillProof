from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from fastapi import Header, HTTPException

DATABASE_URL = "sqlite:///./skillproof.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_auth_uid(x_user_id: str | None = Header(default=None)):
    if not x_user_id:
        raise HTTPException(status_code=401, detail="Sign in required")
    return x_user_id[:180]
