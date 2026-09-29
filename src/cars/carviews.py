from fastapi import  status, HTTPException, Depends, APIRouter
from fastapi.params import Body
from sqlalchemy.exc import IntegrityError
import models
from ..database import get_db
from sqlalchemy.orm import Session
from .. import schemas

router = APIRouter( tags=['Cars'])

def find_index_car(id, cars):
    for i, c in enumerate(cars):
        if c['id'] == id:
            return i
        
@router.get("/cars/")
def getcars(db: Session = Depends(get_db)):

    cars_data = db.query(models.Car).all()

    result = []

    for car in cars_data:
        result.append({
            "id": car.id,
            "model": car.model,
            "colour": car.colour,
            "year": car.year,
            "price": float(car.price),
            "carlocation": car.carlocation,
            "created_at": car.created_at,

            "owner": {
                "id": car.owner.id,
                "email_id": car.owner.email_id,
                "username": car.owner.username
            },

            "brand": {
                "id": car.brand.id,
                "brand": car.brand.brand
            },

            "fueltype": {
                "id": car.fueltype.id,
                "fueltype": car.fueltype.fueltype
            },

            "geartype": {
                "id": car.geartype.id,
                "geartype": car.geartype.geartype
            },

            "post_status": {
                "id": car.post_status.id,
                "status": car.post_status.status
            }
        })

    return result


@router.put("/cars/{carid}/")
def showcars(carid:int,payload : dict = Body(...), db: Session = Depends(get_db)):
    cars = db.query(models.Car)
    index = find_index_car(carid, cars)
    
    if not index:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No cars found by id : {carid}')

    updated_cardata = payload
    updated_cardata['id'] = carid
    # cars[index] = updated_cardata

    return {'message' : "data"}


@router.post("/cars/",status_code=status.HTTP_201_CREATED)
def create(car : schemas.car_creation_form ,db: Session = Depends(get_db)):

    new_car = models.Car(
       owner_id =   car.owner_id,
       brand_id = car.brand_id,
       carlocation =   car.carlocation,
       colour = car.colour,
       fueltype_id =   car.fueltype_id,
       geartype_id = car.geartype_id,
       post_status_id =   car.post_status_id,
       model = car.model,
       year =   car.year,
       price = car.price,
    )  
    db.add(new_car)
    
    try:
            db.commit()
            db.refresh(new_car)
    
    except IntegrityError:
            db.rollback()
    
            raise HTTPException(
                status_code=409,
                detail="Email already exists"
            )
    
    return { "message": "Sales CAR has been created successfully",  "car model": f"{new_car.model}"}
    
@router.delete("/cars/{carid}",status_code=status.HTTP_204_NO_CONTENT)
def deletecars(carid: int, db: Session = Depends(get_db)):
    cars = db.query(models.Car)
    index = find_index_car(carid, cars)
    if not index:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No cars found by id : {carid}')

    return {"message": "Car not found"}
    
