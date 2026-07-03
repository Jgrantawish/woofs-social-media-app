from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel, Relationship

# Create Models which outline the structure of the database tables

class User(SQLModel, table=True):
    # Optional because the database generates the ID so it is of type None until saved
    id: Optional[int] = Field(default=None, primary_key=True)
    # Add indexes to the username and email fields so that look ups are faster. Also ensure they are both unique
    username: str = Field(index=True, unique=True) # why index = True?
    email : str = Field(index=True, unique=True)
    password_hash : str
    # Automatically stamp in the current date and time when a new user is created
    created_date : datetime =  Field(default_factory=datetime.now)
    # Nullable field, users do not have to have a profile picture
    profile_pic_url: Optional[str] = None
    # Nullable field and FK to Location table.
    location_id: Optional[int] = Field(default=None, foreign_key="location.id")

    # Define relationship atrributes of other tables 
    location: "Location" = Relationship(back_populates="users")
    posts: list["Post"] = Relationship(back_populates="user")
    pets: list["Pet"] = Relationship(back_populates="owner")
    comments: list["Comment"] = Relationship(back_populates="user")
    likes: list["Like"] = Relationship(back_populates="user")


class Location(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    city : str
    area : str
    country : str

    users: list[User] = Relationship(back_populates="location")


class Pet(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    owner_id: int = Field(foreign_key="user.id")
    name : str 
    birthday : datetime
    breed : str

    owner: User = Relationship(back_populates="pets")


class Post(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id : int = Field(foreign_key="user.id")
    picture_url : Optional[str] = None
    content : Optional[str] = None
    # Index so that we can sort posts based on their created date 
    created_date : datetime =  Field(default_factory=datetime.now, index=True)
    last_updated : Optional[datetime] = None

    user: User = Relationship(back_populates="posts")
    comments: list["Comment"] = Relationship(back_populates="post")
    likes: list["Like"] = Relationship(back_populates="post")


class Like (SQLModel, table=True):
    user_id : int = Field(primary_key=True, foreign_key="user.id")
    post_id : int = Field(primary_key=True, foreign_key="post.id")

    user: User = Relationship(back_populates="likes")
    post: Post = Relationship(back_populates="likes")


class Comment (SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id : int = Field(foreign_key="user.id")
    post_id : int = Field(foreign_key="post.id")
    content : str
    # Index so that we can sort comments based on their created date 
    created_date : datetime =  Field(default_factory=datetime.now, index=True)
    last_updated : Optional[datetime] = None

    post: Post = Relationship(back_populates="comments")
    user: User = Relationship(back_populates="comments")
