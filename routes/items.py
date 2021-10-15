from fastapi import APIRouter, Depends, status, HTTPException
from database.db import get_db
from sqlalchemy.orm import Session
from schemas import schemas
from models import models
from uuid import UUID
from auth import oauth2

# from fastapi.security import OAuth2PasswordBearer

router = APIRouter(tags=["Ordered Items, Menu and Categories"], prefix="/food")


# Menu based routes


@router.get("/{restaurant_id}/menu", status_code=status.HTTP_200_OK)
async def get_menu_in_restaurant(
    restaurant_id: UUID,
    db: Session = Depends(get_db),
    # user: schemas.User =
    # Depends(oauth2.get_current_user)
):

    menu = db.query(models.Menu).filter(models.Menu.menuid == restaurant_id).all()

    return {"status": status.HTTP_200_OK, "restaurant_id": restaurant_id, "menu": menu}


@router.post("/menu/add", status_code=status.HTTP_201_CREATED)
async def add_menu_item(request: schemas.Menu, db: Session = Depends(get_db)):

    restaurant = (
        db.query(models.Restaurant)
        .filter(models.Restaurant.restaurantid == request.restaurantid)
        .first()
    )

    if not restaurant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find restaurant",
            headers={"WWW-Authenticate": "Bearer"},
        )

    food_category = (
        db.query(models.FoodCategory)
        .filter(models.FoodCategory.foodcategoryid == request.foodcategoryid)
        .first()
    )

    if not food_category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find food category",
            headers={"WWW-Authenticate": "Bearer"},
        )

    new_menu_item = models.Menu(
        restaurant=restaurant,
        foodCategory=food_category,
        Description=request.description,
        Price=request.price,
    )

    db.add(new_menu_item)
    db.commit()
    db.refresh(new_menu_item)

    return {"status": status.HTTP_201_CREATED, "item": new_menu_item}


@router.post("/category/add", status_code=status.HTTP_201_CREATED)
async def add_food_category(
    request: schemas.FoodCategory, db: Session = Depends(get_db)
):
    restaurant = (
        db.query(models.Restaurant)
        .filter(models.Restaurant.name == request.restaurant)
        .first()
    )

    new_category = models.FoodCategory(CategoryName=request.name, restaurant=restaurant)

    db.add(new_category)
    db.commit()
    db.refresh(new_category)

    return {"status": status.HTTP_201_CREATED, "category": new_category}


@router.post("/orderitems/add", status_code=status.HTTP_201_CREATED)
async def add_order_items(
    request: schemas.ItemsOrdered,
    db: Session = Depends(get_db),
    user_jwt: schemas.User = Depends(oauth2.get_current_user),
):

    user = db.query(models.User).filter(models.User.email == user_jwt["sub"]).first()

    orders = db.query(models.Order).filter(models.Order.userid == user.userid).all()

    flag = 0
    concerned_order = None
    for i in orders:
        if i.orderid == request.orderid:
            flag = 1
            concerned_order = i
            break

    if flag == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find order",
            headers={"WWW-Authenticate": "Bearer"},
        )

    new_order_item = models.ItemsOrdered(order=concerned_order, menu=request)

    db.add(new_order_item)
    db.commit()
    db.refresh(new_order_item)

    return {"status": status.HTTP_201_CREATED, "ordered item": new_order_item}
