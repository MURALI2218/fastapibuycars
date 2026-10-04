from fastapi import FastAPI

from .cars import carviews
from .users import userviews
from .chatbot import chatbotviews
from . import models,database

from fastapi.middleware.cors import CORSMiddleware
# models.Base.metadata.create_all(bind = database.engine)

app = FastAPI()

origins = ['*']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins ,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(carviews.router)
app.include_router(userviews.router)
app.include_router(chatbotviews.router)
@app.get("/")
async def root():
    return {"message": "Hello World !!!!"}
 

