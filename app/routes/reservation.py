# app/routes/reservation.py
"""Module process reservation CRUD requests"""

from fastapi import APIRouter, status, HTTPException, Depends
from sqlmodel import Session, select
from app.validate_request import check_user_existence, check_equipment_existence
from app.db import get_session
from ..schemas import action_data_structure as schema_structures


router = APIRouter (prefix = "/reservations", tags = ["Reservations management"])

# add reservation, for URL root/reservations/, code 201 on success
@router.post ("/", status_code = status.HTTP_201_CREATED,
                   response_model = schema_structures.reservation_read)
def create_reservation (reservation: schema_structures.reservation_create,
                        session: Session = Depends (get_session)):
    # check if row with passed user ID already exists
    if not check_user_existence (reservation.user_id, session):
        raise HTTPException (
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"User with ID {reservation.user_id} not found"
        )

    # check if row with passed equipment ID already exists
    if not check_equipment_existence (reservation.equipment_id, session):
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

# patch existing reservation
@router.patch ("/{reservation_id}", status_code = status.HTTP_200_OK,
                                    response_model = schema_structures.reservation_read)
def update_reservation_by_id (reservation_id: int,
                              reservation_patch: schema_structures.reservation_update,
                              session: Session = Depends (get_session)):
    old_reservation = session.get (schema_structures.Reservation, reservation_id)

    # check if row with passed ID already exists
    if not old_reservation:
        raise HTTPException (
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"Reservation with ID {reservation_id} not found"
        )

    # check if there's a new user ID value
    if reservation_patch.user_id:
        # check if row with passed new user ID already exists
        if not check_user_existence (reservation_patch.user_id, session):
            raise HTTPException (
                status_code = status.HTTP_404_NOT_FOUND,
                detail = f"User with ID {reservation_patch.user_id} not found"
            )

    # check if there's a new equipment ID value
    if reservation_patch.equipment_id:
        # check if row with passed equipment ID already exists
        if not check_equipment_existence (reservation_patch.equipment_id, session):
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

# get reservations list
@router.get ("/", status_code = status.HTTP_200_OK,
                  response_model = list [schema_structures.reservation_read])
def read_reservations (session: Session = Depends (get_session)):
    reservations = session.exec (select (schema_structures.Reservation)).all ()

    if reservations is None or len (reservations) == 0:
        raise HTTPException (
            status_code = status.HTTP_204_NO_CONTENT,
            detail = "The reservation list is empty"
        )
    return reservations

# get reservation by ID
@router.get ("/{reservation_id}", status_code = status.HTTP_200_OK,
                                  response_model = schema_structures.reservation_read)
def read_reservation_by_id (reservation_id: int, session: Session = Depends (get_session)):
    reservation = session.get (schema_structures.Reservation, reservation_id)
    if not reservation:
        raise HTTPException (
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"Reservation with ID {reservation_id} not found"
        )
    return reservation

# delete reservation by ID
@router.delete ("/{reservation_id}", status_code = status.HTTP_204_NO_CONTENT)
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
