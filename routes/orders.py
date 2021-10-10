from fastapi import APIRouter, Depends, status
from database.db import get_db
from sqlalchemy.orm import Session
from schemas import schemas
from models import models
import uuid

router = APIRouter(tags=['Orders'])


@router.get('/order/{id}', status_code=status.HTTP_200_OK, response_model=schemas.OrderDetails)
async def get_user(id: int, db: Session = Depends(get_db)):
    entry = db.query(models.Order).filter(models.Order.orderid == id).first()
    return entry
    # return {"details": f"User #{id}"}


@router.post('/makeorder', status_code=status.HTTP_201_CREATED)
async def create_user(request: schemas.Order, db: Session = Depends(get_db)):
    new_order = models.Order(UserId=request.orderid, Name=request.name,
                           ContactNum=request.contactnum, Email=request.email)
    db.add(new_order)
    db.commit()
    db.refresh(new_order)