from fastapi import APIRouter, Depends, status, HTTPException
from database.db import get_db
from sqlalchemy.orm import Session
from schemas import schemas
from models import models
from uuid import UUID

router = APIRouter(prefix="/city", tags=["Cities"])


@router.get("/id/{id}", status_code=status.HTTP_200_OK)
async def get_city_by_id(id: UUID, db: Session = Depends(get_db)):
    city = db.query(models.City).filter(models.City.cityid == id).first()

    if not city:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"City with id {id} not found"
        )

    return city


@router.get("/name/{name}", status_code=status.HTTP_200_OK)
async def get_city_by_name(name: str, db: Session = Depends(get_db)):
    city = db.query(models.City).filter(models.City.cityname == name).first()

    if not city:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"City with name {name} not found",
        )

    return city


@router.post("/add", status_code=status.HTTP_201_CREATED)
async def add_city(request: schemas.City, db: Session = Depends(get_db)):
    new_city = models.City(CityName=request.cityname, StateName=request.statename)

    db.add(new_city)
    db.commit()
    db.refresh(new_city)

    return {"status": status.HTTP_201_CREATED}
