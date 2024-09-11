import secrets

# Функция для генерации уникального секретного ключа
def generate_jwt_secret() -> str:
    """
    Генерирует уникальный JWT секретный ключ.
    
    :return: Секретный ключ для подписи токенов
    """
    return secrets.token_hex(32)  # Генерирует безопасный 256-битный (32 байта) ключ

# Настройки JWT
JWT_SECRET = generate_jwt_secret()  # Генерация нового ключа при каждом запуске
JWT_ALGORITHM = 'HS256'  # Алгоритм для подписи токенов
ACCESS_TOKEN_EXPIRE_MINUTES = 15  # Время жизни access токена в минутах
REFRESH_TOKEN_EXPIRE_DAYS = 7  # Время жизни refresh токена в днях