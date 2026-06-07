from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List


# user
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime
    class Config:
        from_attributes = True

class UserProfile(BaseModel):
    """User + stats follow & jumlah post."""
    id: int
    username: str
    email: str
    created_at: datetime
    followers_count: int
    following_count: int
    posts_count: int
    is_following: bool
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserOut

# comment
class CommentCreate(BaseModel):
    content: str

class CommentOut(BaseModel):
    id: int
    content: str
    created_at: datetime
    post_id: int
    owner_id: int
    owner: UserOut
    class Config:
        from_attributes = True

#post
class PostCreate(BaseModel):
    content: str

class PostUpdate(BaseModel):
    content: str

class PostOut(BaseModel):
    id: int
    content: str
    created_at: datetime
    updated_at: datetime
    owner_id: int
    owner: UserOut
    like_count: int
    comment_count: int
    save_count: int
    is_liked: bool
    is_saved: bool
    comments: List[CommentOut] = []
    class Config:
        from_attributes = True

class FollowOut(BaseModel):
    message: str
    is_following: bool

class LikeOut(BaseModel):
    message: str
    is_liked: bool
    like_count: int

class SaveOut(BaseModel):
    message: str
    is_saved: bool