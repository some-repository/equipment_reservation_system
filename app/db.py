# app/db.py
from sqlmodel import create_engine, Session, SQLModel

DB_URL = "sqlite:///equipment_reservations_database.db"
engine = create_engine (DB_URL, echo = True) # echo is for debugging purpose

def get_session ():
    with Session (engine) as session:
        yield session

def init_database ():
    SQLModel.metadata.create_all (engine)