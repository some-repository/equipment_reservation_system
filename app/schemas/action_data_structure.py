# app/schemas/action_data_structure.py

from datetime import date, timedelta
from pydantic import (BaseModel, Field, BeforeValidator, EmailStr)
from sqlmodel import SQLModel, Field as SQLField

class reservation_base (BaseModel):
    equipment: str
    user: str
    first_date: date
    last_date: date

class reservation_create (reservation_base):
    pass

class reservation_update (BaseModel):
    equipment: str | None = None
    user: str | None = None
    first_date: date | None = None
    last_date: date | None = None
    
class reservation_read (reservation_base):
    reservation_id: int

class Reservation (SQLModel, reservation_base, table = True):
    reservation_id: int = SQLField (default = None, nullable = False, primary_key = True) # redefine attribute to use it as DB primary key
