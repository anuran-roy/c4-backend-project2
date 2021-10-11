from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from database.db import get_db
from schemas import schemas
from models import models
from uuid import UUID

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login")
async def login(request: schemas.Login, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == request.email).first()

    if not user:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid credentials.")

    pass


@router.post("/signup")
async def signup():
    pass


@router.post("/logout")
async def logout():
    pass