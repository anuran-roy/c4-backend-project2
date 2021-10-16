from fastapi import APIRouter, Depends, status, HTTPException
from database.db import get_db
from sqlalchemy.orm import Session
from schemas import schemas

# from auth import oauth2
from models import models
from uuid import UUID

router = APIRouter(tags=["Restaurants"], prefix="/restaurant")


@router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_restaurant(
    id: UUID,
    db: Session = Depends(get_db),
    # user: schemas.User =
    # Depends(oauth2.get_current_user)
):
    restaurant = (
        db.query(models.Restaurant).filter(models.Restaurant.restaurantid == id).first()
    )

    if not restaurant:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Restaurant with id {id} not found",
        )

    return restaurant


@router.get("/city/{name}", status_code=status.HTTP_200_OK)
async def get_restaurant_by_city(
    name: str,
    db: Session = Depends(get_db),
    # user: schemas.User =
    # Depends(oauth2.get_current_user)
):
    city_req = db.query(models.City).filter(models.City.cityname == name).first()
    all_restaurants = (
        db.query(models.Restaurant)
        .filter(models.Restaurant.cityid == city_req.cityid)
        .all()
    )

    return {"Restaurants in your city": all_restaurants}


@router.post("/add", status_code=status.HTTP_201_CREATED)
async def add_restaurant(
    request: schemas.Restaurant,
    db: Session = Depends(get_db),
    # user_jwt: schemas.User =
    # Depends(oauth2.get_current_user)
):
    # if not user_jwt:
    #     raise HTTPException(
    #                         status_code=status.HTTP_401_UNAUTHORIZED,
    #                         detail="Could not validate credentials",
    #                         headers={"WWW-Authenticate": "Bearer"},
    #                        )

    city = db.query(models.City).filter(models.City.cityname == request.city).first()
    new_restaurant = models.Restaurant(
        Name=request.name,
        Address=request.address,
        Rating=request.rating,
        Zipcode=request.zipcode,
        city=city,
    )
    db.add(new_restaurant)
    db.commit()
    db.refresh(new_restaurant)

    return {"status": status.HTTP_201_CREATED, "restaurant": new_restaurant}
