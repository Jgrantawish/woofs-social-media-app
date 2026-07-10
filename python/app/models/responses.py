from datetime import datetime
from sqlmodel import SQLModel
from typing import Optional

# Create Models which outline the structure of Objects that will be sent to the front end 

class CommentResponse (SQLModel):
    id: int
    content: str
    created_date: datetime
    last_updated: Optional[datetime] = None

    owner_username: str
    owner_profile_pic_url: Optional[str] = None
    is_owner: bool

class PostResponse (SQLModel):
    id: int
    picture_url: Optional[str] = None
    content: Optional[str] = None
    created_date: datetime
    last_updated: Optional[datetime] = None

    owner_username: str
    owner_profile_pic_url: Optional[str] = None
    is_owner: bool

    like_count: int
    has_liked: bool

    comment_count: int


class UserResponse(SQLModel):
    id: int
    username: str
    profile_pic_url: Optional[str] = None