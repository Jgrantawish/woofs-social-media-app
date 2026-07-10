from sqlmodel import create_engine, Session
from ..models.models import SQLModel


# Setup the Database Connection
sqlite_url = "sqlite:///woofs.db"
engine = create_engine(sqlite_url)

# Create all of the above tables
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

create_db_and_tables()

# Create all of the above tables
def get_db_session():
    with Session(engine) as session:
        yield session

