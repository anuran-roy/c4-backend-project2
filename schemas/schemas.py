from pydantic import BaseModel  # Base class for request bodies
from datetime import datetime
from typing import Optional
from uuid import UUID

# Input validation schemas ###################################


class City(BaseModel):
    # cityid: Optional[UUID]
    cityname: str
    statename: str


class User(BaseModel):
    # userid: Optional[UUID]
    name: str
    contactnum: str
    email: str
    password: str


class Address(BaseModel):
    # addressid: Optional[UUID]
    title: str

    class Config():
        orm_mode = True


class Order(BaseModel):
    # self.orderid: UUID
    token: str
    restaurantid: UUID
    addressid: UUID
    orderstatus: str
    ordertime: str
    deliverytime: str
    totalitems: int

    class Config():
        orm_mode = True


class Login(BaseModel):
    email: str
    password: str

# Output schemas #############################################


class UserProfile(BaseModel):
    # userId: int
    name: str
    contactnum: str
    email: str

    class Config():
        orm_mode = True


class OrderDetails(BaseModel):
    orderstatus: str
    ordertime: datetime
    deliverytime: datetime
    totalitems: float

    class Config():
        orm_mode = True


class RestaurantProfile(BaseModel):
    address: str
    rating: int
    zipcode: int

    class Config():
        orm_mode = True


class CityDetails(BaseModel):
    cityname: str
    statename: str

    class Config():
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None
