# routes/user.py
from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy import text
from sqlmodel import Session, select
from ..schemas import action_data_structure as schema_structures
from app.db import get_session

router = APIRouter (prefix = "/users", tags = ["Users management"])

@router.post ("/", status_code = status.HTTP_201_CREATED, response_model = schema_structures.user_read) # add user, for URL root/users/, code 201 on success
def create_user (user: schema_structures.user_create, session: Session = Depends (get_session)):
    new_user = schema_structures.User (
        name = user.name,
        email = user.email
    )
    
    session.add (new_user)
    session.commit ()
    session.refresh (new_user)
    return new_user
