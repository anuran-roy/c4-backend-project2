from fastapi import APIRouter, Depends, status, HTTPException
from database.db import get_db
from sqlalchemy.orm import Session
from schemas import schemas
from models import models

# from uuid import UUID
from auth import oauth2

# from fastapi.security import OAuth2PasswordBearer

router = APIRouter(tags=["Payments"], prefix="/pay")


@router.get("/history", status_code=status.HTTP_200_OK)
async def get_payment_history(
    db: Session = Depends(get_db),
    user_jwt: schemas.User = Depends(oauth2.get_current_user),
):

    if not user_jwt:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not verify credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = db.query(models.User).filter(models.User.email == user_jwt["sub"]).first()

    payment_history = (
        db.query(models.Payment).filter(models.Payment.userid == user.userid).all()
    )

    return {"status": status.HTTP_200_OK, "payment history": payment_history}


@router.post("/makepayment", status_code=status.HTTP_201_CREATED)
def make_payment(
    request: schemas.Payment,
    db: Session = Depends(get_db),
    user_jwt: schemas.User = Depends(oauth2.get_current_user),
):

    if not user_jwt:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not verify credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = db.query(models.User).filter(models.User.email == user_jwt["sub"]).first()

    order = (
        db.query(models.Order).filter(models.Order.orderid == request.orderid).first()
    )

    items = (
        db.query(models.ItemsOrdered)
        .filter(models.ItemsOrdered.orderid == order.orderid)
        .all()
    )

    # menus = list()
    tprice = 0

    for i in items:
        # menus.append(db.query(models.Menu)\
        #      .filter(models.Menu.orderid == i.menuid).first())
        tprice += (
            db.query(models.Menu).filter(models.Menu.menuid == i.menuid).first()
        ).price

    new_payment = models.Payment(
        user=user, order=order, AmountToBePaid=tprice, PaymentStatus="unpaid"
    )

    db.add(new_payment)
    db.commit()
    db.refresh(new_payment)

    return {"status": status.HTTP_201_CREATED, "payment info": new_payment}
