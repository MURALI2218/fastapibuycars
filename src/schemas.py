from datetime import datetime
from decimal import Decimal
from typing import Optional,Literal

from pydantic import BaseModel,ConfigDict

class User_Creation(BaseModel):
    username : str
    email_id : str
    password : str 
    contact_number : str

class usercredentials(BaseModel):
    email_id : str
    password : str

class updated_user_form(BaseModel):
    username : str
    email_id : str
    contact_number : str
  
    
class CarDetailsOut(BaseModel):
    id: int
    model: str
    colour: str
    year: int
    price: Decimal
    carlocation: str
    
    owner: UserDetailsOut
    brand: BrandOut
    fueltype: FuelTypeOut
    geartype: GearTypeOut
    post_status: PostStatusDetailsOut
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class UserDetailsOut(BaseModel):
    id: int
    email_id: str
    username: str
    contact_number:str

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


class car_creation_form(BaseModel): 
    brand_id: int
    model: str
    colour: str
    year: int
    price: Decimal
    carlocation: str
    owner_id: int | None = None
    fueltype_id: int
    geartype_id: int
    post_status_id: int

class Token(BaseModel):
    access_token: str
    token_type : str
    

class Tokendata(BaseModel):
    id : Optional[int] = None


class booking_form_input(BaseModel):
    name :str
    contact_number : str
    email_id:str
    carid : int
    

class bookingOut(BaseModel):
    name :str
    contact_number : str
    email_id:str
    car : CarDetailsOut
    bookinguser : UserDetailsOut
    
    model_config = ConfigDict(from_attributes=True)


class RAGRequest(BaseModel):
    query: str


class RAGResponse(BaseModel):
    answer: str


class QueryIntent(BaseModel):
    intent: Literal["car_search", "knowledge"]

class CarSearchFilters(BaseModel):
    brand: Optional[str] = None
    model: Optional[str] = None
    colour: Optional[str] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    fueltype: Optional[str] = None
    geartype: Optional[str] = None
    location: Optional[str] = None
    min_year: Optional[int] = None
    max_year: Optional[int] = None

class CarResponsellm(BaseModel):
    id: int
    brand: str
    model: str
    colour: str
    year: int
    price: float
    carlocation: str | None = None

    model_config = ConfigDict(from_attributes=True)

class CarSearchResponse(BaseModel):
    message: str
    filters: CarResponsellm
    count: int
    cars: list[CarSearchFilters]