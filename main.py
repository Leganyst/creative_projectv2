from database.models.base import Base
from database.init import engine
from app.init import app

Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)