from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel, create_engine, Session

class User(SQLModel, table=True):
    # Optional because the database generates the ID so it is of type None until saved
    id: Optional[int] = Field(default=None, primary_key=True)
    # Add indexes to the username and email fields so that look ups are faster. Also ensure they are both unique
    username: str = Field(index=True, unique=True) # why index = True?
    email : str = Field(index=True, unique=True)
    password_hash : str
    # Automatically stamp in the current date and time when a new user is created
    created_date : datetime =  Field(default_factory=datetime.now())
    # Nullable field, users do not have to have a profile picture
    profile_pic_url: Optional[str] = None
    # Nullable field and FK to Location table.
    location_id: Optional[int] = Field(default=None, foreign_key="location.id")

class Location(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    city : str
    area : str
    country : str

class Pet(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    owner_id: int = Field(foreign_key="user.id")
    name : str 
    birthday : datetime
    breed : str

class Post(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id : int = Field(foreign_key="user.id")
    picture_url : Optional[str] = None
    content : Optional[str] = None
    # Index so that we can sort posts based on their created date 
    created_date : datetime =  Field(default_factory=datetime.now(), index=True)
    last_updated : Optional[datetime] = None

class Like (SQLModel, table=True):
    user_id : int = Field(primary_key=True, foreign_key="user.id")
    post_id : int = Field(primary_key=True, foreign_key="post.id")

class Comment (SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id : int = Field(foreign_key="user.id")
    post_id : int = Field(foreign_key="post.id")
    content : str
    # Index so that we can sort comments based on their created date 
    created_date : datetime =  Field(default_factory=datetime.now(), index=True)
    last_updated : Optional[datetime] = None


# Setup the Database Connection
sqlite_url = "sqlite:///woofs.db"
engine = create_engine(sqlite_url, echo=True) # echo=True shows the raw SQL in your console!

# Create all of the above tables
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

create_db_and_tables()

# create a new user!
#with Session(engine) as session:
    #alice = User(username="alice_gmt", password_hash="hash123", email="alice@here.com")
    #session.add(alice)
    #session.commit()
