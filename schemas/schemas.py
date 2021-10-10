from pydantic import BaseModel # Base class for request bodies
from typing import Optional
from uuid import UUID

################################## Input validation schemas ###################################
class City(BaseModel):
    cityid: Optional[UUID]
    cityname: str
    statename: str

class User(BaseModel):
    userid: Optional[UUID]
    name: str
    contactnum: str
    email: str

class Address(BaseModel):
    addressid: Optional[UUID]
    title: str

    class Config():
        orm_mode = True

class Order(BaseModel):
    pass


############################################ Output schemas #############################################
class UserProfile(BaseModel):
    # userId: int
    name: str
    contactnum: str
    email: str

    class Config():
        orm_mode = True


class OrderDetails(BaseModel):
    pass