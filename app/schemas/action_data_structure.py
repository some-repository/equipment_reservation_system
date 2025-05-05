# app/schemas/action_data_structure.py

from datetime import date, timedelta
from pydantic import (BaseModel, Field, BeforeValidator, EmailStr)
from sqlmodel import SQLModel, Field as SQLField

class user_base (BaseModel):
    name: str
    email: EmailStr

class user_create (user_base):
    pass

class user_read (user_base):
    user_id: int

class User (SQLModel, user_base, table = True): # users table
    user_id: int = SQLField (default = None, nullable = False, primary_key = True) # define ID attribute to use it as table primary key

class reservation_base (BaseModel):
    equipment: str
    user_id: int
    first_date: date
    last_date: date

class reservation_create (reservation_base):
    pass

class reservation_update (BaseModel):
    equipment: str | None = None
    user_id: int | None = None
    first_date: date | None = None
    last_date: date | None = None
    
class reservation_read (reservation_base):
    reservation_id: int

class Reservation (SQLModel, reservation_base, table = True): # reservations table
    reservation_id: int = SQLField (default = None, nullable = False, primary_key = True) # define ID attribute to use it as table primary key
