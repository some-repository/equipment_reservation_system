# app/routes/user.py
"""Module process user CRUD requests"""

from fastapi import APIRouter, status, Depends, HTTPException
from sqlmodel import Session, select
from app.db import get_session
from ..schemas import action_data_structure as schema_structures

router = APIRouter (prefix = "/users", tags = ["Users list management"])

# add user, for URL root/users/, code 201 on success
@router.post ("/", status_code = status.HTTP_201_CREATED,
                   response_model = schema_structures.user_read)
def create_user (user: schema_structures.user_create,
                 session: Session = Depends (get_session)):
    new_user = schema_structures.User (
        name = user.name,
        email = user.email
    )

    session.add (new_user)
    session.commit ()
    session.refresh (new_user)
    return new_user

# get users list
@router.get ("/", status_code = status.HTTP_200_OK,
                  response_model = list [schema_structures.user_read])
def read_users (session: Session = Depends (get_session)):
    users = session.exec (select (schema_structures.User)).all ()

    if users is None or len (users) == 0:
        raise HTTPException (
            status_code = status.HTTP_204_NO_CONTENT,
            detail = "The user list is empty"
        )
    return users