from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, UniqueConstraint
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    posts     = relationship("Post",    back_populates="owner",    cascade="all, delete")
    comments  = relationship("Comment", back_populates="owner",    cascade="all, delete")
    likes     = relationship("Like",    back_populates="user",     cascade="all, delete")
    saves     = relationship("Save",    back_populates="user",     cascade="all, delete")