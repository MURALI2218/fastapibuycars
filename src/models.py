from sqlalchemy import Boolean, Column, Integer, Numeric, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy.sql.sqltypes import TIMESTAMP 
from sqlalchemy.sql.expression import text

from .database import Base
# -------------------------
# Brand
# -------------------------
class Brand(Base):
    __tablename__ = "brands"

    id = Column(Integer, primary_key=True)
    brand = Column(String, nullable=False)

    cars = relationship("Car", back_populates="brand")


# -------------------------
# Fuel Type
# -------------------------
class FuelType(Base):
    __tablename__ = "fuel_types"

    id = Column(Integer, primary_key=True)
    fueltype = Column(String, nullable=False)

    cars = relationship("Car", back_populates="fueltype")

# -------------------------
# Gear Type
# -------------------------
class GearType(Base):
    __tablename__ = "gear_types"

    id = Column(Integer, primary_key=True)
    geartype = Column(String, nullable=False)

    cars = relationship("Car", back_populates="geartype")

# -------------------------
# Post Status
# -------------------------
class PostStatus(Base):
    __tablename__ = "post_status"

    id = Column(Integer, primary_key=True)
    status = Column(String, nullable=False)

    cars = relationship("Car", back_populates="post_status")

# -------------------------
# User Table Model
# -------------------------
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email_id = Column(String, nullable=False)
    username = Column(String, nullable=False)
    contact_number = Column(String,nullable=True, default=None)
    password = Column(String, nullable=False)

    cars = relationship("Car", back_populates="owner")
# -------------------------
# Car
# -------------------------
class Car(Base):
    __tablename__ = "cars"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    model = Column(String, nullable=False)
    colour = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    price = Column(Numeric(12, 2), nullable=False)
    carlocation = Column(String, nullable=False)
    

    owner_id = Column( Integer, ForeignKey("users.id"),nullable=False)
    brand_id = Column(Integer,ForeignKey("brands.id"),nullable=False)
    fueltype_id = Column(Integer,ForeignKey("fuel_types.id"),nullable=False)
    geartype_id = Column(Integer,ForeignKey("gear_types.id"),nullable=False)
    post_status_id = Column(Integer,ForeignKey("post_status.id"),nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)
    
    # Relationships
    owner = relationship("User", back_populates="cars")
    brand = relationship("Brand", back_populates="cars")
    fueltype = relationship("FuelType", back_populates="cars")
    geartype = relationship("GearType", back_populates="cars")
    post_status = relationship("PostStatus", back_populates="cars")

    booking = relationship("carbooking", back_populates="cardetail")

# -------------------------
# Car BOOKING MODEL
# -------------------------

class carbooking(Base):
    __tablename__ = "bookings"

    bookingid = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    contact_number = Column(String, nullable=False)
    emailid = Column(String, nullable=False)
    booking_userid = Column(Integer,nullable=False)
    car_id =  Column(Integer, ForeignKey("cars.id"), nullable=False)
    # Relationships
    cardetail = relationship("Car", back_populates="booking")

