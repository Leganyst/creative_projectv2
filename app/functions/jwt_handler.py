import jwt
import datetime

from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


from app.config import JWT_SECRET, JWT_ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS

security = HTTPBearer()

def create_access_token(user_id: str) -> str:
    """
    Создает JWT access токен.
    
    :param user_id: Идентификатор пользователя для включения в токен
    :return: Строка access токена
    """
    expiration = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "user_id": user_id,
        "exp": expiration
    }
    access_token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return access_token

def create_refresh_token(user_id: str) -> str:
    """
    Создает JWT refresh токен с большим сроком жизни.
    
    :param user_id: Идентификатор пользователя для включения в токен
    :return: Строка refresh токена
    """
    expiration = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    payload = {
        "user_id": user_id,
        "exp": expiration
    }
    refresh_token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return refresh_token

def decode_token(token: str) -> dict:
    """
    Декодирует токен и возвращает payload.
    
    :param token: JWT токен
    :return: Декодированный payload в виде словаря
    """
    try:
        decoded_payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

def refresh_access_token(refresh_token: str) -> str:
    """
    Обновляет access токен с использованием refresh токена.
    
    :param refresh_token: JWT refresh токен
    :return: Новый access токен
    """
    payload = decode_token(refresh_token)
    user_id = payload.get("user_id")
    if not user_id:
        raise Exception("Invalid refresh token")
    
    return create_access_token(user_id)

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    """
    Декодирует и проверяет валидность JWT токена.
    Используется как зависимость в маршрутах FastAPI.
    
    :param credentials: Авторизационные креды (токен)
    :return: Декодированные данные пользователя
    """
    token = credentials.credentials.replace("Bearer ", "")
    return decode_token(token)