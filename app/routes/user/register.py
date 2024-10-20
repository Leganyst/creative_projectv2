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
    
    # Проверяем наличие пользователя с таким email
    try:
        user_in_db = get_user_from_db(session, user.email)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")
    except ValueError:
        pass
    
    # Создаем запись пользователя в базе
    user_in_db = User(**user.model_dump(exclude={"profession", "address", "birthdate"}))
    session.add(user_in_db)
    session.commit()  # Сохраняем пользователя сначала

    # Если указана профессия, создаем мастера
    if user.profession:
        master_data = {
            "profession": user.profession,
            "address": user.address,  # Адрес, если есть
            "birthdate": user.birthdate  # Дата рождения, если есть
        }
        user_in_db.master = Master(**{key: value for key, value in master_data.items() if value is not None})
        session.add(user_in_db.master)
        session.commit()  # Сохраняем мастера

    return UserModel.model_validate(user_in_db)
