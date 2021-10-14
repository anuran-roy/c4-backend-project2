from fastapi import APIRouter, Depends, status, HTTPException
from database.db import get_db
from sqlalchemy.orm import Session
# from schemas import schemas
from models import models
from uuid import UUID

router = APIRouter(tags=['Restaurants'], prefix="/restaurant")


@router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_restaurant(id: UUID, db: Session = Depends(get_db)):
    restaurant = db.query(models.Restaurant).filter(
                models.Restaurant.restaurantid == id).first()

    if not restaurant:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f"Restaurant with id {id} not found")

    return restaurant


@router.post("/add", status_code=status.HTTP_201_CREATED)
async def add_restaurant(request, db: Session = Depends(get_db)):
    new_restaurant = models.Restaurant()
    db.add(new_restaurant)
    db.commit()
    db.refresh(new_restaurant)
