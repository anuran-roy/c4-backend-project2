from fastapi import APIRouter, Depends, status, HTTPException
from database.db import get_db
from sqlalchemy.orm import Session
from schemas import schemas
from models import models
from uuid import UUID
from auth import oauth2

# from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta


router = APIRouter(tags=["Orders"], prefix="/orders")


@router.get(
    "/order/{id}", status_code=status.HTTP_200_OK, response_model=schemas.OrderDetails
)
async def get_order_by_id(
    id: UUID,
    db: Session = Depends(get_db),
    user: schemas.User = Depends(oauth2.get_current_user),
):
    order = db.query(models.Order).filter(models.Order.orderid == id).first()

    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order with id {id} not found.",
        )

    return order
    # return {"details": f"User #{id}"}


@router.post("/makeorder", status_code=status.HTTP_201_CREATED)
async def create_order(
    request: schemas.Order,
    db: Session = Depends(get_db),
    user_jwt: schemas.User = Depends(oauth2.get_current_user),
    # current_user = Depends(oauth2.get_current_user)
):

    if not user_jwt:
        print("\n\nCredentials exception raised from orders.py\n")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = db.query(models.User).filter(models.User.email == user_jwt["sub"]).first()

    restaurant = (
        db.query(models.Restaurant)
        .filter(models.Restaurant.restaurantid == request.restaurant_id)
        .first()
    )

    address = (
        db.query(models.Address)
        .filter(models.Address.addressid == request.customer_address_id)
        .first()
    )

    new_order = models.Order(
        OrderStatus="preparing",
        OrderTime=str(datetime.now()),
        DeliveryTime=str(datetime.now() + timedelta(minutes=30)),
        restaurant=restaurant,
        address=address,
        user=user,
        TotalItems=request.totalitems,
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    return {"status": status.HTTP_201_CREATED, "user": user, "order": new_order}


@router.get("/history", status_code=status.HTTP_200_OK)
async def get_order_history(
    db: Session = Depends(get_db),
    user_jwt: schemas.User = Depends(oauth2.get_current_user),
):
    if user_jwt is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = db.query(models.User).filter(models.User.email == user_jwt["sub"]).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user",
            headers={"WWW-Authenticate": "Bearer"},
        )
    order_history = (
        db.query(models.Order).filter(models.Order.userid == user.userid).all()
    )

    return {"status": status.HTTP_201_CREATED, "order history": order_history}


# @router.post("/additems", status_code=status.HTTP_201_CREATED)
# async def additems(request,
#                    db: Session = Depends(get_db),
#                    user_jwt: schemas.User = Depends(oauth2.get_current_user)
#                    ):
#     pass
