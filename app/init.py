from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.user.register import register_router
from app.routes.user.auth import auth_router
from app.routes.user.update_user import update_user_router
from app.routes.user.get_me import get_me_router

app = FastAPI()

# Разрешаем все CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешаем все источники
    allow_credentials=True,
    allow_methods=["*"],  # Разрешаем все HTTP методы
    allow_headers=["*"],  # Разрешаем все заголовки
)

app.include_router(register_router)
app.include_router(auth_router)
app.include_router(update_user_router)
app.include_router(get_me_router)