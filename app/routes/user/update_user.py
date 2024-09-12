from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.functions.jwt_handler import get_current_user
from app.models.user import UpdateUserModel, UserModel
from app.depends.verified_user import get_user_from_token
from database.models.user import User, Master
from database.init import get_db

update_user_router = APIRouter()

@update_user_router.patch("/api/user/update/", tags=["user"])
async def update_user(
    update_data: UpdateUserModel,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_db),
    user_in_db: User = Depends(get_user_from_token)
):
    """
    Обновление данных пользователя: имени, почты, телефона и профессии для мастера.
    """    
    user = user_in_db

    # Обновление данных пользователя
    if update_data.name:
        user.name = update_data.name
    if update_data.email:
        user.email = update_data.email.lower()
    if update_data.phone_number:
        user.phone_number = update_data.phone_number

    # Если пользователь является мастером, обновляем профессию
    if update_data.profession:
        if user.master:
            user.master.profession = update_data.profession
        else:
            # Если пользователь не был мастером, создаём запись для мастера
            user.master = Master(profession=update_data.profession, user_id=user.id)
            session.add(user.master)

    session.commit()

    return UserModel.model_validate(user)
