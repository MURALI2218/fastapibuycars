import time
from . import config

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_URL = (
    f"postgresql://"
    f"{config.settings.database_username}:"
    f"{config.settings.database_password}@"
    f"{config.settings.database_hostname}:"
    f"{config.settings.database_port}/"
    f"{config.settings.database_name}"
)
engine = create_engine(SQLALCHEMY_URL)

SessionLocal = sessionmaker(autocommit = False, autoflush= False, bind = engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception:
        raise
    finally:
        db.close()


import psycopg2
from psycopg2.extras import RealDictCursor

while True:
    try:
        conn = psycopg2.connect(host=f'{config.settings.database_hostname}', port = 22304,database = f'{config.settings.database_name}', user=f'{config.settings.database_username}', password= f'{config.settings.database_password}', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("connection successful")
        break
    except Exception as error:
        print(f"Connection UnSuccessful :: {error}")
        

