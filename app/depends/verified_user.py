from fastapi import Depends
from sqlalchemy.orm import Session

from app.functions.jwt_handler import decode_token
from database.models.user import User

def get_user_from_db_depend(session: Session, payload: dict = Depends(decode_token)) -> User:
    user_id = payload.get("user_id")
    if not user_id:
        raise ValueError("Invalid token")
    user = session.query(User).filter(User.id == user_id).first()
    if not user:
        raise ValueError("User not found")
    return user

