from app.schemas import action_data_structure as schema_structures
from app.db import get_session
from fastapi import Depends
from sqlmodel import Session

def check_user_existence (user_id: int, session: Session = Depends (get_session)):
    user = session.get (schema_structures.User, user_id)
    if not user:
        return False
    else:
        return True