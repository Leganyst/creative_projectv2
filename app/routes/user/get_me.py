from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.depends.verified_user import get_user_from_token  # Зависимость для получения текущего пользователя
from database.init import get_db
from database.models.user import User
from app.models.user import UserModel

get_me_router = APIRouter()

@get_me_router.get("/api/user/me/", tags=["user"], response_model=UserModel)
async def get_me(current_user: User = Depends(get_user_from_token),
                 session: Session = Depends(get_db)):
    """
    Получение данных о текущем пользователе (getme).
    """
    # Возвращаем информацию о пользователе
    return UserModel.model_validate(current_user)