from fastapi import status,HTTPException, Depends, APIRouter
from ..database import get_db
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import schemas, utils, models
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(tags=["users"])


@router.post("/createuser")
def create_user(user: schemas.User_Creation,db: Session = Depends(get_db)):
    hashed_password = utils.hash_password(user.password)

    new_user = models.User(
        username = user.username,
        email_id=user.email_id,
        password=hashed_password
    )

    db.add(new_user)

    try:
        db.commit()
        db.refresh(new_user)

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=409,
            detail="Email already exists"
        )

    return { "message": "User created successfully",  "emailid": new_user.email_id}

