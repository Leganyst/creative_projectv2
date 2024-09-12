from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.functions.hashing import verify_password
from app.functions.jwt_handler import create_access_token, create_refresh_token, refresh_access_token, get_current_user
from app.depends.verified_user import get_user_from_db_depend_auth
from database.functions.user import get_user_from_db
from database.init import get_db
from app.models.user import LoginUser, TokenModel

auth_router = APIRouter()

# Эндпоинт для авторизации пользователя и выдачи токенов
@auth_router.post("/api/user/auth/", tags=["user"], response_model=TokenModel)
async def authenticate_user(user: LoginUser, session: Session = Depends(get_db), user_in_db = Depends(get_user_from_db_depend_auth)):
    """
    Авторизация пользователя и выдача токенов.
    """
    # Создаем access и refresh токены
    access_token = create_access_token(user_id=user_in_db.id)
    refresh_token = create_refresh_token(user_id=user_in_db.id)

    return {"access_token": access_token, "refresh_token": refresh_token}


# Эндпоинт для обновления access токена с помощью refresh токена
@auth_router.post("/api/user/refresh/", tags=["user"], response_model=TokenModel)
async def refresh_token(credentials: dict = Depends(get_current_user)):
    """
    Обновление access токена с помощью refresh токена.
    """
    refresh_token = credentials.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No refresh token provided")

    # Обновляем access токен
    new_access_token = refresh_access_token(refresh_token)

    return {"access_token": new_access_token, "refresh_token": refresh_token}
