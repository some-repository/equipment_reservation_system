# app/routes/reservation.py
from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy import text
from sqlmodel import Session, select
from ..schemas import action_data_structure as schema_structures
from app.db import get_session
from app.validate_request import check_user_existence, check_equipment_existence

router = APIRouter (prefix = "/reservations", tags = ["Reservations management"])

@router.post ("/", status_code = status.HTTP_201_CREATED, response_model = schema_structures.reservation_read) # add reservation, for URL root/reservations/, code 201 on success
def create_reservation (reservation: schema_structures.reservation_create, session: Session = Depends (get_session)):
    if not check_user_existence (reservation.user_id, session): # check if row with passed user ID already exists
        raise HTTPException (
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"User with ID {reservation.user_id} not found"
        )
    
    if not check_equipment_existence (reservation.equipment_id, session): # check if row with passed equipment ID already exists
        raise HTTPException (
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"Equipment with ID {reservation.equipment_id} not found"
        )
    
    new_reservation = schema_structures.Reservation (
        equipment_id = reservation.equipment_id,
        user_id = reservation.user_id,
        first_date = reservation.first_date,
        last_date = reservation.last_date
    )
    
    session.add (new_reservation)
    session.commit ()
    session.refresh (new_reservation)
    return new_reservation

@router.patch ("/{reservation_id}", status_code = status.HTTP_200_OK, response_model = schema_structures.reservation_read) # patch existing reservation
def update_reservation_by_id (reservation_id: int, reservation_patch: schema_structures.reservation_update, session: Session = Depends (get_session)): 
    old_reservation = session.get (schema_structures.Reservation, reservation_id)

    if not old_reservation: # check if row with passed ID already exists
        raise HTTPException (
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"Reservation with ID {reservation_id} not found"
        )
    
    if reservation_patch.user_id: # check if there's a new user ID value
        if not check_user_existence (reservation_patch.user_id, session): # check if row with passed new user ID already exists
            raise HTTPException (
                status_code = status.HTTP_404_NOT_FOUND,
                detail = f"User with ID {reservation_patch.user_id} not found"
            )
    
    if reservation_patch.equipment_id: # check if there's a new equipment ID value
        if not check_equipment_existence (reservation_patch.equipment_id, session): # check if row with passed equipment ID already exists
            raise HTTPException (
                status_code = status.HTTP_404_NOT_FOUND,
                detail = f"Equipment with ID {reservation_patch.equipment_id} not found"
            )

    new_data = reservation_patch.model_dump (exclude_unset = True)
    old_reservation.sqlmodel_update (new_data)
    session.add (old_reservation)
    session.commit ()
    session.refresh (old_reservation)

    return old_reservation

@router.get ("/", status_code = status.HTTP_200_OK, response_model = list [schema_structures.reservation_read]) # get reservations list
def read_reservations (session: Session = Depends (get_session)):
    reservations = session.exec (select (schema_structures.Reservation)).all ()

    if reservations is None or len (reservations) == 0:
        raise HTTPException (
            status_code = status.HTTP_204_NO_CONTENT,
            detail = f"The reservation list is empty"
        )
    return reservations

@router.get ("/{reservation_id}", status_code = status.HTTP_200_OK, response_model = schema_structures.reservation_read) # get reservation by ID
def read_reservation_by_id (reservation_id: int, session: Session = Depends (get_session)):
    reservation = session.get (schema_structures.Reservation, reservation_id)
    if not reservation:
        raise HTTPException (
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"Reservation with ID {reservation_id} not found"
        )
    return reservation

@router.delete ("/{reservation_id}", status_code = status.HTTP_204_NO_CONTENT) # delete reservation by ID
def delete_reservation_by_id (reservation_id: int, session: Session = Depends (get_session)):
    reservation = session.get (schema_structures.Reservation, reservation_id)
    if not reservation:
        raise HTTPException (
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"Reservation with ID {reservation_id} not found"
        )
    
    session.delete (reservation)
    session.commit ()

    return {"ok": True}
