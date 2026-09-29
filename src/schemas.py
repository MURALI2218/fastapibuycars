from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel,ConfigDict

class User_Creation(BaseModel):
    username : str
    email_id : str
    password : str 

class usercredentials(BaseModel):
    email_id : str
    password : str

class UserDetailsOut(BaseModel):
    id: int
    email_id: str
    username: str

    model_config = ConfigDict(from_attributes=True)


class PostStatusDetailsOut(BaseModel):
    id: int
    status: str

    model_config = ConfigDict(from_attributes=True)


class GearTypeOut(BaseModel):
    id: int
    geartype: str

    model_config = ConfigDict(from_attributes=True)


class FuelTypeOut(BaseModel):
    id: int
    fueltype: str

    model_config = ConfigDict(from_attributes=True)


class BrandOut(BaseModel):
    id: int
    brand: str

    model_config = ConfigDict(from_attributes=True)
    
class CarDetailsOut(BaseModel):
    id: int
    model: str
    colour: str
    year: int
    price: Decimal
    carlocation: str

    owner_id: UserDetailsOut
    brand: BrandOut
    fueltype: FuelTypeOut
    geartype: GearTypeOut
    post_status: PostStatusDetailsOut
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class car_creation_form(BaseModel): 
    brand_id: int
    model: str
    colour: str
    year: int
    price: Decimal
    carlocation: str
    owner_id: int
    fueltype_id: int
    geartype_id: int
    post_status_id: int

class User_Creation(BaseModel):
    username : str
    email_id : str
    password : str 


