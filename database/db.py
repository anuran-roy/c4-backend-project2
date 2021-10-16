from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from decouple import config

DB_PATH = config("DB_PATH")

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
