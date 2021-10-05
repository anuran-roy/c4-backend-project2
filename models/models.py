from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.sql.sqltypes import Boolean
from database.db import Base
from sqlalchemy.orm import relationship

class City(Base):

    __tablename__ = 'city'
    cityId = Column(Integer, primary_key=True, index=True)
    cityName = Column(String)
    stateName = Column(String)
    addresses = relationship("City", back_populates="city")
    restaurants = relationship("Restaurant", back_populates="city")
    # 2 outgoing connections

class User(Base):

    __tablename__ = 'user'
    userId = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    contactNum = Column(String)
    email = Column(String)
    addresses = relationship("Address", back_populates="user")
    orders = relationship("Order", back_populates="user")
    payments = relationship("Payment", back_populates="user")
    # 3 outgoing connections

class Address(Base):

    __tablename__ = 'address'
    addressId = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    zipcode = Column(Integer)
    currentAddress = Column(String)
    street = Column(String)
    userId = Column(Integer, ForeignKey('user.userId'))  # Foreign Key
    cityId = Column(Integer, ForeignKey('city.cityId'))  # Foreign Key
    user = relationship("User", back_populates="addresses")
    city = relationship("City", back_populates="addresses")
    orders = relationship("Order", back_populates="address")
    # One towards order. So 2 incoming connections (requires Foreign Key), 1 outgoing.

class Restaurant(Base):

    __tablename__ = 'restaurant'

    restaurantId = Column(Integer, primary_key=True, index=True)
    address = Column(String)
    rating = Column(Integer)
    zipcode = Column(Integer)
    cityId = Column(Integer, ForeignKey('city.cityId'))  # Foreign Key
    city = relationship("City", back_populates="restaurants")
    menus = relationship("Menu", back_populates="restaurant")
    foodCategories = relationship("FoodCategory", back_populates="restaurant")
    orders = relationship("Order", back_populates="restaurant")
    # 3 outgoing connections, 1 incoming from city (requires Foreign Key)

class Menu(Base):

    __tablename__ = 'menu'

    menuId = Column(Integer, primary_key=True)
    restaurantId = Column(Integer, ForeignKey('restaurant.restaurantId'))  # Foreign Key
    foodCategoryId = Column(Integer, ForeignKey('foodCategory.foodCategoryId'))  # Foreign Key
    description = Column(String)
    price = Column(Integer)
    restaurant = relationship("Restaurant", back_populates="menus")
    foodCategory = relationship("FoodCategory", back_populates="menus")
    menu = relationship("ItemsOrdered", back_populates="items")
    prices = relationship("ItemsOrdered", back_populates="itemsPrice")
    #2 incoming (requires foreign key), 2 outgoing.

class FoodCategory(Base):

    __tablename__ = 'foodcategory'

    foodCategoryId = Column(Integer, primary_key=True)
    restaurantId = Column(Integer, ForeignKey('restaurant.restaurantId'))  # Foreign Key
    categoryName = Column(String)
    restaurant = relationship("Restaurant", back_populates="foodCategories")
    menu = relationship("Menu", back_populates="foodCategory")
    # 1 incoming, 1 outgoing connection

class Payment(Base):

    __tablename__ = 'payment'

    paymentId = Column(Integer, primary_key=True)
    userId = Column(Integer, ForeignKey('user.userId'))  # Foreign Key
    orderId = Column(Integer, ForeignKey('order.orderId'))  # Foreign Key
    amountToBePaid = Column(Float)
    paymentStatus = Column(String)
    user = relationship('User', back_populates="payments")
    correspondingOrder = relationship("Order", back_populates="payment")
    # 1 incoming, 1 outgoing

class Order(Base):

    __tablename__ = 'order'

    orderId = Column(Integer, primary_key=True)
    userId = Column(Integer, ForeignKey('user.userId'))  # Foreign Key
    restaurantId = Column(Integer, ForeignKey('restaurant.restaurantId'))  # Foreign Key
    addressId = Column(Integer, ForeignKey('address.addressId'))  # Foreign Key
    orderStatus = Column(String)
    orderTime = Column(DateTime)
    deliveryTime = Column(DateTime)
    totalItems = Column(Float)
    user = relationship("User", back_populates="orders")
    restaurant = relationship("Restaurant", back_populates="orders")
    itemsOrdered = relationship("ItemsOrdered", back_populates="orders")
    address = relationship("Address", back_populates="orders")
    payment = relationship("Payment", back_populates="correspondingOrder")
    # 4 incoming, 1 outgoing

class ItemsOrdered(Base):

    __tablename__ = 'itemsOrdered'

    itemsOrderedId = Column(Integer, primary_key=True)
    orderId = Column(Integer, ForeignKey('order.orderId'))  # Foreign Key
    menuId = Column(Integer, ForeignKey('menu.menuId'))  # Foreign Key

    quantity = Column(Integer)
    prices = relationship("Menu", back_populates="price")
    orders = relationship("Order", back_populates="itemsOrdered")
    # menu = relationship("")
    # 3 incoming, 1 outgoing