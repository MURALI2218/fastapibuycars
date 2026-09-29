from fastapi import FastAPI, status, HTTPException, Depends
from fastapi.params import Body
from sqlalchemy.exc import IntegrityError

from .cars import carviews
from .users import userviews

from sqlalchemy.orm import Session
from .database import get_db
from . import models,database

models.Base.metadata.create_all(bind = database.engine)

app = FastAPI()
app.include_router(carviews.router)
app.include_router(userviews.router)
@app.get("/")
async def root():
    return {"message": "Hello World !!!!"}
 

