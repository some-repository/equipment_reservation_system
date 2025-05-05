# app/routes/user.py
from fastapi import APIRouter, status, Depends
from sqlmodel import Session
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
