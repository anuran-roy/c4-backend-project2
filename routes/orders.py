from fastapi import APIRouter, Depends, status, HTTPException
from database.db import get_db
from sqlalchemy.orm import Session
from schemas import schemas
from models import models
from uuid import UUID
from auth import oauth2
from fastapi.security import OAuth2PasswordBearer

router = APIRouter(tags=['Orders'])


@router.get('/order/{id}', status_code=status.HTTP_200_OK,
            response_model=schemas.OrderDetails)
async def get_user(id: UUID, db: Session = Depends(get_db),
                   user: schemas.User = Depends(oauth2.get_current_user)):
    order = db.query(models.Order).filter(models.Order.orderid == id).first()

    if not order:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f"Order with id {id} not found.")

    return order
    # return {"details": f"User #{id}"}


@router.post('/makeorder', status_code=status.HTTP_201_CREATED)
async def create_order(request: schemas.Order, db: Session = Depends(get_db),
                      user: schemas.User = Depends(oauth2.get_current_user)):
    user = oauth2.get_current_user(request.token)

    if not user:
        raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # new_order = models.Order(OrderStatus="preparing", OrderTime=)
    # db.add(new_order)
    # db.commit()
    # db.refresh(new_order)

    return {
            "status": status.HTTP_201_CREATED,
            "user": user.__dict__
           }
