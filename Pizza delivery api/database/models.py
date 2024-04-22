from database.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey
from sqlalchemy_utils import ChoiceType 

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(30), unique=True)
    email = Column(String(100), unique=True)
    password = Column(Text, nullable=True)
    is_staff = Column(Boolean, default=False)
    is_active = Column(Boolean, default=False)

    orders = relationship('Order', back_populates="user") 

    def __repr__(self):
        return f"<User {self.username}>"

class Order(Base):
    __tablename__ = 'orders'

    ORDER_STATUS = (
        ("PENDING", "pending"),
        ("IN-TRANSIT", "in-transit"),
        ("DELIVERED", "delivered"), 
    )

    PIZZA_SIZE = (
        ("SMALL", "small"),
        ("MEDIUM", "medium"),
        ("LARGE", "large"),
        ("EXTRA-LARGE", "extra-large"),
    )

    id = Column(Integer, primary_key=True, index=True)
    quantity = Column(Integer, nullable=False)
    order_status = Column(ChoiceType(ORDER_STATUS), default="PENDING")  
    pizza_size = Column(ChoiceType(PIZZA_SIZE), default="SMALL")  
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship('User', back_populates="orders") 

    def __repr__(self):
        return f"<Order {self.id}>"
