# app/routes/equipment.py
"""Module process equipment CRUD requests"""

from fastapi import APIRouter, status, Depends, HTTPException
from sqlmodel import Session, select
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

# get equipments list
@router.get ("/", status_code = status.HTTP_200_OK,
                  response_model = list [schema_structures.equipment_read])
def read_equipments (session: Session = Depends (get_session)):
    equipments = session.exec (select (schema_structures.Equipment)).all ()

    if equipments is None or len (equipments) == 0:
        raise HTTPException (
            status_code = status.HTTP_204_NO_CONTENT,
            detail = "The equipment list is empty"
        )
    return equipments
