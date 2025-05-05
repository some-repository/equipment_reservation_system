# app/routes/equipment.py
"""Module process equipment CRUD requests"""

from fastapi import APIRouter, status, Depends
from sqlmodel import Session
from app.db import get_session
from ..schemas import action_data_structure as schema_structures

router = APIRouter (prefix = "/equipment", tags = ["Equipment list management"])

# add equipment, for URL root/users/, code 201 on success
@router.post ("/", status_code = status.HTTP_201_CREATED,
                   response_model = schema_structures.equipment_read)
def create_equipment (equipment: schema_structures.equipment_create,
                      session: Session = Depends (get_session)):
    new_equipment = schema_structures.Equipment (
        designation = equipment.designation,
        quantity = equipment.quantity
    )

    session.add (new_equipment)
    session.commit ()
    session.refresh (new_equipment)
    return new_equipment
