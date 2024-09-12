from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.functions.jwt_handler import decode_token
from database.models.user import User
from app.models.user import LoginUser
from app.functions.hashing import verify_password
from database.functions.user import get_user_from_db
from database.init import get_db

security = HTTPBearer()

def get_user_from_token(credentials: HTTPAuthorizationCredentials = Depends(security), session: Session = Depends(get_db)) -> User:
    """
    Извлекает токен из заголовка Authorization, раскодирует его и получает пользователя по user_id.
    
    :param credentials: Авторизационные креды из заголовка
    :param session: Сессия для работы с БД
    :return: Объект пользователя
    """
    token = credentials.credentials.replace("Bearer ", "")
    try:
        payload = decode_token(token)
        user_id = payload.get("user_id")
        if not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token: no user_id")
        
        # Получаем пользователя по user_id
        user = session.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
        return user
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


async def get_user_from_db_depend_auth(user: LoginUser, session: Session = Depends(get_db)) -> User:
    """
    Получаем пользователя из базы данных при авторизации

    Args:
        user (LoginUser): Данные для авторизации
        session (Session): Объект сессии БД. Defaults to Depends(get_db).

    Raises:
        HTTPException: Пользователь не найден
        HTTPException: Невалидный токен

    Returns:
        User: Модель пользователя в БД
    """
    user_in_db = get_user_from_db(session, user.email)
    if not user_in_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    if not verify_password(user.password, user_in_db.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect password")

    return user_in_db