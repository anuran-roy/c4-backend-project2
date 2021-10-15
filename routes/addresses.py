from fastapi import APIRouter, Depends, status, HTTPException
from database.db import get_db
from sqlalchemy.orm import Session
from schemas import schemas
from models import models

# from uuid import UUID
from auth import oauth2

router = APIRouter(prefix="/address", tags=["Address"])


@router.post("/add", status_code=status.HTTP_201_CREATED)
def add_new_address(
    request: schemas.Address,
    db: Session = Depends(get_db),
    user_jwt: schemas.User = Depends(oauth2.get_current_user),
):
    user = db.query(models.User).filter(models.User.email == user_jwt["sub"]).first()
    city = db.query(models.City).filter(models.City.cityname == request.city).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if city is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find city",
            headers={"WWW-Authenticate": "Bearer"},
        )

    new_address = models.Address(
        Name=request.name,
        ZipCode=request.zipcode,
        Street=request.street,
        user=user,
        city=city,
    )

    db.add(new_address)
    db.commit()
    db.refresh(new_address)

    return {"status": status.HTTP_201_CREATED, "address": new_address}
