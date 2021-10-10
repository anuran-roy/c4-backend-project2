from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.sql.sqltypes import Boolean
from database.db import Base, db
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid

class City(Base):

    __tablename__ = 'city'
    cityid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    cityname = Column(String)
    statename = Column(String)
    # addresses = relationship("City", back_populates="city")
    # restaurants = relationship("Restaurant", back_populates="city")
    # 2 outgoing connections

    def __init__(self, CityId, CityName, StateName):
        self.cityid = CityId
        self.cityname = CityName
        self.statename = StateName


class User(Base):

    __tablename__ = 'user'
    userid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String)
    contactnum = Column(String)
    email = Column(String)

    def __init__(self, UserId, Name, ContactNum, Email):
        self.userid = UserId
        self.name = Name
        self.contactnum = ContactNum
        self.email = Email

    # addresses = relationship("Address", back_populates="user")
    # orders = relationship("Order", back_populates="user")
    # payments = relationship("Payment", back_populates="user")
    # 3 outgoing connections


class Address(Base):

    __tablename__ = 'address'
    addressid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String)
    zipcode = Column(Integer)
    currentaddress = Column(String)
    street = Column(String)
    userid = Column(UUID(as_uuid=True), ForeignKey('user.userid'))  # Foreign Key
    cityid = Column(UUID(as_uuid=True), ForeignKey('city.cityid'))  # Foreign Key

    def __init__(self,AddressId, Name, ZipCode, CurrentAddress, Street):
        self.addressid = AddressId
        self.name = Name
        self.zipcode = ZipCode
        self.currentaddress = CurrentAddress
        self.street = Street
        self.userid = user.userid
        self.cityid = city.cityid

    # user = relationship("User", back_populates="addresses")
    # city = relationship("City", back_populates="addresses")
    # orders = relationship("Order", back_populates="address")
    # One towards order. So 2 incoming connections (requires Foreign Key), 1 outgoing.


class Restaurant(Base):

    __tablename__ = 'restaurant'

    restaurantid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    address = Column(String)
    rating = Column(Integer)
    zipcode = Column(Integer)
    cityid = Column(UUID(as_uuid=True), ForeignKey('city.cityid'))  # Foreign Key

    def __init__(self, RestaurantId, Address, Rating, Zipcode):
        self.restaurantid = RestaurantId
        self.address = Address
        self.rating = Rating
        self.zipcode = Zipcode
        self.cityid = city.cityid
    # city = relationship("City", back_populates="restaurants")
    # menus = relationship("Menu", back_populates="restaurant")
    # foodCategories = relationship("FoodCategory", back_populates="restaurant")
    # orders = relationship("Order", back_populates="restaurant")
    # 3 outgoing connections, 1 incoming from city (requires Foreign Key)


class FoodCategory(Base):

    __tablename__ = 'foodCategory'

    foodcategoryid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    restaurantid = Column(UUID(as_uuid=True), ForeignKey('restaurant.restaurantid'))  # Foreign Key
    categoryname = Column(String)
    # restaurant = relationship("Restaurant", back_populates="foodCategories")
    # menus = relationship("Menu", back_populates="foodCategory")
    # 1 incoming, 1 outgoing connection

    def __init__(self,FoodCategoryId, CategoryName):
        self.foodcategoryid = FoodCategoryId
        self.categoryname = CategoryName
        self.restaurantid = restaurant.restaurantid


class Menu(Base):

    __tablename__ = 'menu'

    menuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    restaurantid = Column(UUID(as_uuid=True), ForeignKey('restaurant.restaurantid'))  # Foreign Key
    foodcategoryid = Column(UUID(as_uuid=True), ForeignKey('foodCategory.foodcategoryid'))  # Foreign Key
    description = Column(String)
    price = Column(Integer)

    def __init__(self, MenuId, Description, Price):
        self.menuid = MenuId
        self.restaurantid = restaurant.restaurantid
        self.foodcategoryid = foodCategory.foodcategoryid
        self.description = Description
        self.price = Price

    # restaurant = relationship("Restaurant", back_populates="menus")
    # foodCategory = relationship("FoodCategory", back_populates="menus")
    # menu = relationship("ItemsOrdered", back_populates="items")
    # prices = relationship("ItemsOrdered", back_populates="itemsPrice")
    #2 incoming (requires foreign key), 2 outgoing.


class Payment(Base):

    __tablename__ = 'payment'

    paymentid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    userid = Column(UUID(as_uuid=True), ForeignKey('user.userid'))  # Foreign Key
    orderid = Column(UUID(as_uuid=True), ForeignKey('order.orderid'))  # Foreign Key
    amounttobepaid = Column(Float)
    paymentstatus = Column(String)

    def __init__(self, PaymentId, AmountToBePaid, PaymentStatus):
        self.paymentid = PaymentId
        self.userid = user.userid
        self.orderid = order.orderid
        self.amounttobepaid = AmountToBePaid
        self.paymentstatus = PaymentStatus
    # user = relationship('User', back_populates="payments")
    # correspondingOrder = relationship("Order", back_populates="payment")
    # 1 incoming, 1 outgoing


class Order(Base):

    __tablename__ = 'order'

    orderid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    userid = Column(UUID(as_uuid=True), ForeignKey('user.userid'))  # Foreign Key
    restaurantid = Column(UUID(as_uuid=True), ForeignKey('restaurant.restaurantid'))  # Foreign Key
    addressid = Column(UUID(as_uuid=True), ForeignKey('address.addressid'))  # Foreign Key
    orderstatus = Column(String)
    ordertime = Column(DateTime)
    deliverytime = Column(DateTime)
    totalitems = Column(Float)

    def __init__(self, OrderId, OrderStatus, OrderTime, DeliveryTime, TotalItems):
        self.orderid = OrderId
        self.restaurantid = restaurant.restaurantid
        self.addressid = address.addressid
        self.orderstatus = OrderStatus
        self.ordertime = OrderTime
        self.deliverytime = DeliveryTime
        self.totalitems = TotalItems

    # user = relationship("User", back_populates="orders")
    # restaurant = relationship("Restaurant", back_populates="orders")
    # itemsOrdered = relationship("ItemsOrdered", back_populates="orders")
    # address = relationship("Address", back_populates="orders")
    # payment = relationship("Payment", back_populates="correspondingOrder")
    # 4 incoming, 1 outgoing


class ItemsOrdered(Base):

    __tablename__ = 'itemsOrdered'

    itemsorderedid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    orderid = Column(UUID(as_uuid=True), ForeignKey('order.orderid'))  # Foreign Key
    menuid = Column(UUID(as_uuid=True), ForeignKey('menu.menuid'))  # Foreign Key

    quantity = Column(Integer)

    def __init__(self, ItemsOrderedId):
        self.itemsorderedid = ItemsOrderedId
        self.orderid = order.orderid
        self.menuid = menu.menuid
    # prices = relationship("Menu", back_populates="price")
    # orders = relationship("Order", back_populates="itemsOrdered")
    # menu = relationship("")
    # 3 incoming, 1 outgoing

########################### Defining Relationships ###########################



########################### Reflecting the changes in DB ###########################

Base.metadata.create_all(db)