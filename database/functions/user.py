from sqlalchemy.orm import Session

from database.models.user import User

def get_user_from_db(session: Session, email: int) -> User:
    """
    Получаем пользователя из БД по его user_id

    Args:
        session (Session): объект Сессии с БД
        user_id (int): id пользователя

    Raises:
        ValueError: Пользователь не найден в базе

    Returns:
        User: Модель пользователя в базе данных
    """
    user = session.query(User).filter(User.email == email).first()
    if not user:
        raise ValueError("User not found")
    return user