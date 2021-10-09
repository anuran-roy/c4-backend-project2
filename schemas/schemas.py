from pydantic import BaseModel # Base class for request bodies
from typing import Optional

class City(BaseModel):
    cityid: int
    cityname: str
    statename: str

class User(BaseModel):
    userid: int
    name: str
    contactnum: str
    email: str

class Address(BaseModel):
    title: str

    class Config():
        orm_mode = True

# class User(BaseModel):
#     name: str
#     username: str
#     email: str
#     password: str

class UserProfile(BaseModel):
    # userId: int
    name: str
    contactnum: str
    email: str

    class Config():
        orm_mode = True