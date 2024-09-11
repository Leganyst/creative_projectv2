import bcrypt

def hash_password(password: str) -> str:
    """
    Хэширует пароль с использованием bcrypt.
    
    :param password: Строка пароля для хэширования
    :return: Захэшированный пароль
    """
    # Генерируем соль
    salt = bcrypt.gensalt()
    # Возвращаем хэш пароля
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')

def verify_password(password: str, hashed_password: str) -> bool:
    """
    Проверяет, соответствует ли введенный пароль хэшу.
    
    :param password: Введенный пользователем пароль
    :param hashed_password: Хэшированный пароль из базы данных
    :return: True, если пароли совпадают, иначе False
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
