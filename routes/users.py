from fastapi import APIRouter, Depends, status, HTTPException
from database.db import get_db
from sqlalchemy.orm import Session
from schemas import schemas
from models import models
from uuid import UUID

# from auth import oauth2

router = APIRouter(prefix="/user", tags=["Users"])


@router.get("/id/{id}", response_model=schemas.UserProfile)
def get_user_by_id(id: UUID, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.userid == id).first()

    if not user:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with the id {id} is not found.",
        )

    return user
    # return {"details": f"User #{id}"}


@router.get("/{email_or_phno}", response_model=schemas.UserProfile)
def get_user_by_details(email_or_phno: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == email_or_phno).first()

    if user is not None:
        return user

    user = db.query(models.User).filter(models.User.contactnum == email_or_phno).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User with given detail is not found.",
        )

    return user
