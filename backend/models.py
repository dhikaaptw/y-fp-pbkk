from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, UniqueConstraint
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime


class Follow(Base):
    __tablename__ = "follows"
    __table_args__ = (UniqueConstraint("follower_id", "following_id"),)

    id = Column(Integer, primary_key=True, index=True)
    follower_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    following_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


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

    following = relationship("Follow", foreign_keys=[Follow.follower_id],
                             backref="follower", cascade="all, delete")
    followers = relationship("Follow", foreign_keys=[Follow.following_id],
                             backref="following_user", cascade="all, delete")


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


class Comment(Base):
    """Komentar pada sebuah post."""
    __tablename__ = "comments"

    id         = Column(Integer, primary_key=True, index=True)
    content    = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    post_id    = Column(Integer, ForeignKey("posts.id"), nullable=False)
    owner_id   = Column(Integer, ForeignKey("users.id"), nullable=False)

    post  = relationship("Post", back_populates="comments")
    owner = relationship("User", back_populates="comments")


class Like(Base):
    __tablename__ = "likes"
    __table_args__ = (UniqueConstraint("user_id", "post_id"),)

    id      = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)

    user = relationship("User", back_populates="likes")
    post = relationship("Post", back_populates="likes")


class Save(Base):
    __tablename__ = "saves"
    __table_args__ = (UniqueConstraint("user_id", "post_id"),)

    id      = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)

    user = relationship("User", back_populates="saves")
    post = relationship("Post", back_populates="saves")