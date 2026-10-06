from fastapi import  status, HTTPException, Depends, APIRouter
from fastapi.params import Body
from sqlalchemy.exc import IntegrityError

from ..database import get_db
from sqlalchemy.orm import Session
from .. import schemas, models, auth2
from typing import List

router = APIRouter( tags=['Cars'])

def find_index_car(id, cars):
    for i, c in enumerate(cars):
        if c['id'] == id:
            return i
        
@router.get("/api/cars/")
def getcars(db: Session = Depends(get_db)):

    cars_data = db.query(models.Car)
    cars_data1 = db.query(models.Car).first()
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


@router.put("/api/cars/{carid}/")
def update_car(carid: int,car: schemas.car_creation_form,db: Session = Depends(get_db),get_current_user: dict = Depends(auth2.get_current_user)
):
    car_data = db.query(models.Car).filter(models.Car.id == carid,models.Car.owner_id == get_current_user.id).first()

    if not car_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No car found by id: {carid}"
        )

    # Convert Pydantic object to dictionary
    update_data = car.model_dump()

    # Update SQLAlchemy object
    for field, value in update_data.items():
        setattr(car_data, field, value)
    car_data.owner_id = get_current_user.id

    db.commit()
    db.refresh(car_data)

    return {
        "message": "Car data updated successfully"
    }
@router.post("/api/cars/",status_code=status.HTTP_201_CREATED, )
def create(car : schemas.car_creation_form ,db: Session = Depends(get_db), get_current_user :dict = Depends(auth2.get_current_user)):
    print(car)
    new_car = models.Car(
       owner_id =   get_current_user.id,
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

    except IntegrityError as error:
        db.rollback()

        raise HTTPException(
            status_code=409,
            detail=str(error.orig)
        )
    return { "message": "Sales CAR has been created successfully",  "car model": f"{new_car.model}"}
   
        # print("========== DATABASE ERROR ==========")
        # print("ERROR:", error)
        # print("ORIGINAL:", error.orig)
        # print("====================================")
 
@router.delete("/api/cars/{carid}/", status_code=status.HTTP_204_NO_CONTENT)
def deletecars(carid: int, db: Session = Depends(get_db), get_current_user :dict = Depends(auth2.get_current_user)):
    car = db.query(models.Car).filter(models.Car.id == carid and models.Car.owner_id == get_current_user.id).first()
    if not car:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No cars found by id : {carid}')
    
    db.delete(car)
    db.commit()
    return { "message" : f"{car.model} has been deleted"}

                    # ------------------------#
                    #     BOOKING SECTION     #
                    # ------------------------#

@router.post("/api/carbooking/")
def bookcars(bookingdetial : schemas.booking_form_input, db : Session =Depends(get_db), current_user : dict = Depends(auth2.get_current_user)):
    careatedbookingid = db.query(models.carbooking).filter(
            models.carbooking.booking_userid == current_user.id,
            models.carbooking.car_id == bookingdetial.carid
        ).first()

    if careatedbookingid :
        raise HTTPException(status_code=409, detail="You have already booked this car so please check the details you have entered")
    
    new_booking = models.carbooking(
                booking_userid =   current_user.id,
                name = bookingdetial.name,
                contact_number = bookingdetial.contact_number,
                emailid = bookingdetial.email_id,
                car_id  = bookingdetial.carid
     )
    db.add(new_booking)
         
    try:
        db.commit()
        db.refresh(new_booking)
         
    except IntegrityError as error:
        db.rollback()
       
        raise HTTPException(status_code=409,detail = str(error.orig))

    careatedbookingid = db.query(models.carbooking).filter(
        models.carbooking.booking_userid == current_user.id,
        models.carbooking.car_id == bookingdetial.carid
    ).first()
    
         
    return { "message": " CAR has been successfully booked",  "car booking id": f"{careatedbookingid.bookingid}"}
         
@router.get("/api/carbooking/",response_model=List[schemas.bookingOut])
def bookcars(db: Session = Depends(get_db),current_user: dict = Depends(auth2.get_current_user)):

    bookings = db.query(models.carbooking).filter(
        models.carbooking.booking_userid == current_user.id
    ).all()

    results = []

    for booking in bookings:

        car = db.query(models.Car).filter(
            models.Car.id == booking.car_id
        ).first()

        user = db.query(models.User).filter(
            models.User.id == booking.booking_userid
        ).first()

        results.append({
            "name": booking.name,
            "contact_number": booking.contact_number,
            "email_id": booking.emailid,
            "car": car,
            "bookinguser": user
        })

    return results
    


@router.get("/api/geartype/")
def geartype( db : Session =Depends(get_db), current_user : dict = Depends(auth2.get_current_user)) :
     return db.query(models.GearType).all()

     

@router.get("/api/fueltype/")
def fueltype(
    db: Session = Depends(get_db),
    current_user: dict = Depends(auth2.get_current_user)
):
    return db.query(models.FuelType).all()

    

@router.get("/api/brand/", response_model=list[schemas.BrandOut])
def brand(
    db: Session = Depends(get_db),
    current_user: dict = Depends(auth2.get_current_user)
):
    return db.query(models.Brand).all()


@router.get("/api/poststatus/", response_model=list[schemas.PostStatusDetailsOut])
def poststatus(
    db: Session = Depends(get_db),
    current_user: dict = Depends(auth2.get_current_user)
):
    return db.query(models.PostStatus).all()

@router.get("/api/usersalescars/")
def usersalescardetails(db: Session =Depends(get_db), current_user: dict = Depends(auth2.get_current_user)):
    usersalescars = db.query(models.Car).filter(models.Car.owner_id == current_user.id)

    result = []
    
    for car in usersalescars:
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

