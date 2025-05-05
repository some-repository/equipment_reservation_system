# app/validate_request.py
from fastapi import Depends
from sqlmodel import Session
from app.db import get_session
from app.schemas import action_data_structure as schema_structures

def check_user_existence (user_id: int, session: Session = Depends (get_session)):
    user = session.get (schema_structures.User, user_id)
    if not user: # if row with passed ID wasn't found in User table
        return False
    else:
        return True

def check_equipment_existence (equipment_id: int, session: Session = Depends (get_session)):
    equipment = session.get (schema_structures.Equipment, equipment_id)
    if not equipment: # if row with passed ID wasn't found in Equipment table
        return False
    else:
        return True
    