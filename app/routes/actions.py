# routes/actions.py
from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy import text
from sqlmodel import Session, select
from ..schemas import action_data_structure as schema_structures
from app.db import get_session

router = APIRouter (prefix = "/reservations", tags = ["Reservations management"])

#@router.get ("/test-db", status_code = status.HTTP_200_OK) # test database
#def test_database (session: Session = Depends (get_session)):
#    result = session.exec (select(text("'Random text'"))).fetchall ()
#    return result

@router.post ("/", status_code = status.HTTP_201_CREATED) # add reservation, for URL root/reservations/, code 201 on success
def create_reservation (reservation: schema_structures.reservation_create, session: Session = Depends (get_session)):
    new_reservation = schema_structures.Reservation (
        equipment = reservation.equipment,
        user = reservation.user,
        first_date = reservation.first_date,
        last_date = reservation.last_date
    )
    
    session.add (new_reservation)
    session.commit ()
    session.refresh (new_reservation)
    return new_reservation

@router.patch ("/{reservation_id}", status_code = status.HTTP_200_OK, response_model = schema_structures.reservation_read) # patch existing reservation
def update_reservation_by_id (reservation_id: int, reservation_patch: schema_structures.reservation_update, session: Session = Depends (get_session)):
    #reservation_fields = set (schema_structures.equipment_reservation.model_fields.keys ())

    #if not set (new_data.keys ()) <= reservation_fields: # validate request by checking if all keys of new_data are fields of equipment_reservation 
    #    raise HTTPException (
    #        status_code = status.HTTP_400_BAD_REQUEST,
    #        detail = f"An update request must only contain"
    #                 f" one or more of the following fields:"
    #                 f" {", ".join (reservation_fields)}"
    #    )
    
    old_reservation = session.get (schema_structures.Reservation, reservation_id)

    if not old_reservation: # check if row with passed ID already exist
        raise HTTPException (
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"Reservation with ID {reservation_id} not found"
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
