from fastapi import APIRouter, Depends, HTTPException, Body
from sqlmodel import Session, select
from ..database.database import get_db_session
from ..models.models import User
from ..core.security import hash_password
import re

router = APIRouter()
router = APIRouter(prefix="/auth")

def get_user_by_username(db_session: Session, username: str):
    return db_session.exec(
        select(User).where(User.username == username)
    ).first()

def get_user_by_email(db_session: Session, email: str):
    return db_session.exec(
        select(User).where(User.email == email)
    ).first()

def validate_new_username(db_session: Session, username: str):
    MIN_LENGTH = 3
    MAX_LENGTH = 20
    # Check username is of an appropriate length
    if len(username) < MIN_LENGTH or len(username) > MAX_LENGTH:
        raise HTTPException(
            status_code=400,
            detail="Invalid username" 
        )

    # Check username doesnt contain spaces
    if any(char.isspace() for char in username):
        raise HTTPException(
            status_code=400,
            detail="Username cannot contain spaces"
        )

    # Check username isn't already in use
    if get_user_by_username(db_session,username):
        raise HTTPException(
            status_code=400,
            detail="Username already taken"
        )

def validate_new_email(db_session: Session, email: str):
    EMAIL_REGEX = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")

    # Check email matches the format of something@something.something with no spaces
    if not EMAIL_REGEX.match(email):
        raise HTTPException(
            status_code=400,
            detail="Invalid email address"
        )
    
    # Check email isn't already in use
    if get_user_by_email(db_session,email):
        raise HTTPException(
            status_code=400,
            detail="Email address already taken"
        )
    

# GET endpoint for checking username availability
# Used for frontend validation during signup
@router.get("/users/check-username")
def check_username(
    username: str,
    session: Session = Depends(get_session)
):
    user = get_user_by_username(session, username)
    
    return {
        "available": user is None
    }

# GET endpoint for checking email availability
# Used for frontend validation during signup
@router.get("/users/check-email")
def check_email(
    email: str,
    session: Session = Depends(get_session)
):
    user = get_user_by_email(session, email)
    
    return {
        "available": user is None
    }

# POST endpoint for creating a new user
# Used on the signup page to register a new account
@router.post("/signup")
def signup(
    username: str = Body(...),
    email: str = Body(...),
    password: str = Body(...),
    session: Session = Depends(get_session)
):
    validate_new_username(session, username)
    validate_new_email(session, email)
    hashed_password = hash_password(password)

    new_user = User(
        username=username,
        email=email,
        password_hash=hashed_password
    )

    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return {
        "message": "User created",
        "user_id": new_user.id
    }