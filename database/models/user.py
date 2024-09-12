from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

from database.models.base import Base

class User(Base):
    __tablename__ = 'users'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False)
    phone_number: Mapped[str] = mapped_column(nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    master = relationship('Master', back_populates='user', uselist=False)

class Master(Base):
    __tablename__ = 'masters'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    user = relationship('User', back_populates='master', uselist=False)
    # Лучше бы предлагать варианты, но да ладно, и так сойдет пока
    profession: Mapped[str] = mapped_column(nullable=False)