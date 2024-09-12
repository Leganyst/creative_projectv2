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
    master: MasterModel | None = Field(default=None, description="Мастер, если пользователь является мастером")
    
    class Config:
        from_attributes = True
    
    
class RegisterUser(BaseModel):
    name: str = Field(description="Логин (фамилия-имя) пользователя", example="Иван Плюшков")
    email: str = Field(description="Email пользователя", example="test_example@mail.com")
    phone_number: str = Field(description="Номер телефона пользователя", example="+79991234567")
    password: str = Field(description="Пароль пользователя", example="12345678")
    profession: str | None = Field(default=None, description="Профессия мастера", example="Парикмахер")
    
    
class LoginUser(BaseModel):
    email: str
    password: str

class TokenModel(BaseModel):
    access_token: str
    refresh_token: str

class UpdateUserModel(BaseModel):
    name: str | None = Field(description="Логин (фамилия-имя) пользователя", example="Иван Плюшков")
    email: str | None = Field(description="Email пользователя", example="test_example@mail.com")
    phone_number: str | None = Field(description="Номер телефона пользователя", example="+79991234567")
    profession: str | None = Field(default=None, description="Профессия мастера", example="Парикмахер")
