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

class Post(Base):
    __tablename__ = "posts"

    id         = Column(Integer, primary_key=True, index=True)
    content    = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    owner_id   = Column(Integer, ForeignKey("users.id"), nullable=False)

    owner    = relationship("User",    back_populates="posts")
    comments = relationship("Comment", back_populates="post", cascade="all, delete")
    likes    = relationship("Like",    back_populates="post", cascade="all, delete")
    saves    = relationship("Save",    back_populates="post", cascade="all, delete")