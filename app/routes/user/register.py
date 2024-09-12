from os import name
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.depends.verified_user import get_user_from_db_depend_auth
from app.functions.hashing import hash_password
from app.models.user import RegisterUser, UserModel
from database.functions.user import get_user_from_db
from database.init import get_db
from database.models.user import Master, User


register_router = APIRouter()

@register_router.post("/api/user/register/", tags=["user"], response_model=UserModel)
async def register_user(user: RegisterUser,
                        session: Session = Depends(get_db)):
    user.email = user.email.lower()
    user.password = hash_password(user.password)
    try:
        user_in_db = get_user_from_db(session, user.email)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")
    except ValueError:
        pass
    
    user_in_db = User(**user.model_dump(exclude={"profession"}))
    session.add(user_in_db)
    session.commit()
    
    if user.profession:
        user_in_db.master = Master(profession=user.profession)
        session.add(user_in_db.master)
        session.commit()
    
    return UserModel.model_validate(user_in_db)