# app/routes/equipment.py
from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy import text
from sqlmodel import Session, select
from ..schemas import action_data_structure as schema_structures
from app.db import get_session

router = APIRouter (prefix = "/equipment", tags = ["Equipment list management"])

@router.post ("/", status_code = status.HTTP_201_CREATED, response_model = schema_structures.equipment_read) # add equipment, for URL root/users/, code 201 on success
def create_equipment (equipment: schema_structures.equipment_create, session: Session = Depends (get_session)):
    new_equipment = schema_structures.Equipment (
        designation = equipment.designation,
        quantity = equipment.quantity
    )
    
    session.add (new_equipment)
    session.commit ()
    session.refresh (new_equipment)
    return new_equipment
