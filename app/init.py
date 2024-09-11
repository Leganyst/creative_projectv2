from fastapi import FastAPI

from app.routes.user.register import register_router

app = FastAPI()

app.include_router(register_router)