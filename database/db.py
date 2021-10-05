from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DB_PATH = "postgresql://postgres:password@127.0.0.1:5432/c4-backend-project2"

db = create_engine(DB_PATH, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db)

Base = declarative_base()