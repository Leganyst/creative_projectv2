from fastapi import FastAPI

from app.routes.user.register import register_router
from app.routes.user.auth import auth_router
from app.routes.user.update_user import update_user_router

app = FastAPI()

app.include_router(register_router)
app.include_router(auth_router)
app.include_router(update_user_router)