from typing import Optional
from pydantic import BaseModel, Field


class MasterModel(BaseModel):
    id: int = Field(description="ID Мастера", example=432)
    user_id: int = Field(description="ID как пользователя", example=432)
    profession: str = Field(description="Профессия мастера", example="Парикмахер")
    
    class Config:
        from_attributes = True


class UserModel(BaseModel):
    id: int = Field(description="ID Пользователя", example=432)
    name: str = Field(description="Логин (фамилия-имя) пользователя", example="Иван Плюшков")
    email: str = Field(description="Email пользователя", example="test_example@mail.com")
    phone_number: str = Field(description="Номер телефона пользователя", example="+79991234567")
    master: Optional[MasterModel] = Field(default=None, description="Мастер, если пользователь является мастером")
    
    class Config:
        from_attributes = True
    
    
class RegisterUser(BaseModel):
    name: str = Field(description="Логин (фамилия-имя) пользователя", example="Иван Плюшков")
    email: str = Field(description="Email пользователя", example="test_example@mail.com")
    phone_number: str = Field(description="Номер телефона пользователя", example="+79991234567")
    password: str = Field(description="Пароль пользователя", example="12345678")
    profession: Optional[str] = Field(default=None, description="Профессия мастера", example="Парикмахер")
    