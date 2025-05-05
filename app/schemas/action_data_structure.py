# app/schemas/action_data_structure.py

from datetime import date, timedelta
from pydantic import (BaseModel, Field, BeforeValidator, EmailStr)
from sqlmodel import SQLModel, Field as SQLField

# user-related classes
class user_base (BaseModel):
    name: str
    email: EmailStr

class user_create (user_base):
    pass

class user_read (user_base):
    user_id: int

class User (SQLModel, user_base, table = True): # users table
    user_id: int = SQLField (default = None, nullable = False, primary_key = True) # define ID attribute to use it as table primary key

# equipment-related classes
class equipment_base (BaseModel):
    designation: str
    quantity: int

class equipment_create (equipment_base):
    pass

class equipment_read (equipment_base):
    equipment_id: int

class Equipment (SQLModel, equipment_base, table = True): # equipment table
    equipment_id: int = SQLField (default = None, nullable = False, primary_key = True) # define ID attribute to use it as table primary key

# reservation-related classes
class reservation_base (BaseModel):
    equipment_id: int
    user_id: int
    first_date: date
    last_date: date

class reservation_create (reservation_base):
    pass

class reservation_update (BaseModel):
    equipment_id: int | None = None # None allows to update only a part of attributes
    user_id: int | None = None
    first_date: date | None = None
    last_date: date | None = None
    
class reservation_read (reservation_base):
    reservation_id: int

class Reservation (SQLModel, reservation_base, table = True): # reservations table
    reservation_id: int = SQLField (default = None, nullable = False, primary_key = True) # define ID attribute to use it as table primary key
