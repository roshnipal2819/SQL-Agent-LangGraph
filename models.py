import os
from dotenv import load_dotenv
from sqlalchemy import Column, Integer, String, ForeignKey, Float, create_engine
from sqlalchemy.orm import relationship, declarative_base, sessionmaker

# Load environment variables
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///example.db")

# Set up SQLAlchemy database engine
Base = declarative_base()
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer)
    email = Column(String, unique=True)
    orders = relationship("Order", back_populates="user")


class Food(Base):
    __tablename__ = "food"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    price = Column(Float)
    orders = relationship("Order", back_populates="food")


class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    food_id = Column(Integer, ForeignKey("food.id"))
    user = relationship("User", back_populates="orders")
    food = relationship("Food", back_populates="orders")


# Create tables
Base.metadata.create_all(bind=engine)
