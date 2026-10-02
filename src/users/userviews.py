from fastapi import status,HTTPException, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from ..database import get_db
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from .. import schemas, utils, models
from sqlalchemy.orm import Session
from ..database import get_db
from ..auth2 import create_access_token
from .. import auth2

router = APIRouter(tags= ['users'])

from pwdlib import PasswordHash
password_hash = PasswordHash.recommended()

def hash_password(password : str):
    return password_hash.hash(password)

def verify_password(entered_password, dbpassword):
    return password_hash.verify(entered_password, dbpassword)

@router.post("/api/createuser/")
def create_user(user: schemas.User_Creation,db: Session = Depends(get_db)):

    hashed_password = hash_password(user.password)

    new_user = models.User(
        username = user.username,
        email_id = user.email_id,
        password = hashed_password,
        contact_number = user.contact_number
    )

    db.add(new_user)

    try:
        db.commit()
        db.refresh(new_user)

    except IntegrityError:
        db.rollback()

        raise HTTPException(status_code=409, detail="Email already exists")

    return { "message": "User created successfully",  "emailid": new_user.email_id}



@router.put('/api/updateusers/{userid}/')
def updateuserdetails(updateduserdetails:schemas.updated_user_form,userid : int, db : Session=Depends(get_db), current_user: dict = Depends(auth2.get_current_user)):
    user_detail = db.query(models.User).filter(
        models.User.id == userid ,
        models.User.id == current_user.id
        ).first()
    if not user_detail:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No car found by id: {userid}"
            )
    # Convert Pydantic object to dictionary
    update_data = updateduserdetails.model_dump()
    
    # Update SQLAlchemy object
    for field, value in update_data.items():
        setattr(user_detail, field, value)
    user_detail.id = current_user.id
    
    db.commit()
    db.refresh(user_detail)
    
    return {
            "message": " profile details updated successfully"
        }



@router.get("/api/userprofile/{user_id}/", response_model=schemas.UserDetailsOut)
def profiledetails(user_id :int,  db : Session=Depends(get_db), current_user: dict = Depends(auth2.get_current_user)):
    user_details = db.query(models.User).filter(
        models.User.id == user_id , 
        models.User.id == current_user.id
        ).first()
    
    if not user_details:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= f"No user found by id: {user_id}"
              )
    
    return user_details

# @router.get("/userprofile/{user_id}/", response_model=schemas.UserDetailsOut)
# def profiledetails(
#     user_id: int,
#     db: Session = Depends(get_db),
#     current_user: dict = Depends(auth2.get_current_user)
# ):
#     user_details = db.query(models.User).filter(
#         models.User.id == user_id,
#         models.User.id == current_user.id
#     ).first()

#     if not user_details:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"No user found by id: {user_id}"
#         )

#     return user_details


@router.post("/api/login/", response_model=schemas.Token)
def login_user(user:OAuth2PasswordRequestForm = Depends(),db: Session = Depends(get_db)):
    user_data = db.query(models.User).filter(
        models.User.email_id == user.username
        ).first()
    
    # User doesn't exist
    if user_data is None:
        raise HTTPException(status_code=401, detail="email not found please enter correct mailid")

    # Check password
    if not verify_password  (user.password,user_data.password):
        raise HTTPException(status_code=401, detail="Invalid password")

    access_token = create_access_token(data={"userid" :user_data.id, "username" : user_data.username})

    return access_token