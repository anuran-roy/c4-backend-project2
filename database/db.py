from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DB_PATH = "postgresql://postgres:password@127.0.0.1:5432/c4_backend_project2"

db = create_engine(DB_PATH)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db)

Base = declarative_base()


def get_db():
    db = SessionLocal()

    try:
        print("Accessing DB...")
        yield db
    finally:
        db.close()
