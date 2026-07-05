from fastapi import APIRouter, Depends, HTTPException, Body
from sqlmodel import Session, select
from ..database.database import get_db_session
from ..models.models import User
from ..core.security import hash_password, verify_password
from ..core.sessions import cookie, SessionData, create_user_session, get_user_session, delete_user_session
from uuid import UUID
import re
from fastapi import Response


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
    db_session: Session = Depends(get_db_session)
):
    user = get_user_by_username(db_session, username)
    
    return {
        "available": user is None
    }


# GET endpoint for checking email availability
# Used for frontend validation during signup
@router.get("/users/check-email")
def check_email(
    email: str,
    db_session: Session = Depends(get_db_session)
):
    user = get_user_by_email(db_session, email)
    
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
    db_session: Session = Depends(get_db_session)
):
    validate_new_username(db_session, username)
    validate_new_email(db_session, email)
    hashed_password = hash_password(password)

    new_user = User(
        username=username,
        email=email,
        password_hash=hashed_password
    )

    db_session.add(new_user)
    db_session.commit()
    db_session.refresh(new_user)

    return {"message": "User created"}


# POST endpoint for logging into an account
# Verify user and create a session 
@router.post("/login")
async def login(
    response: Response,
    username: str = Body(...),
    password: str = Body(...),
    db_session: Session = Depends(get_db_session)
):
    user = get_user_by_username(db_session, username)

    # If username exists in the db, check that the password matches
    if user:
        correct_password = verify_password(password, user.password_hash)
  
    # If no username or wrong password, invalid credentials
    if user is None or not correct_password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Create a session for the user
    user_session = await create_user_session(user.id, user.username, user.profile_pic_url)

    # Attach cookie to response so that the browser knows that the session exists
    cookie.attach_to_response(response, user_session)

    return {"message": "Logged In"}


# GET endpoint for checking theat the user has a valid session
# Called by the AuthGaurd on the front end to stop unauthenticated users from being able to access specific pages 
@router.get("/check-session")
def check_session(user_session: SessionData = Depends(get_user_session)):
    return user_session

# POST endpoint for logging a user out of their account
@router.post("/logout")
async def logout(
    response: Response,
    session_id: UUID = Depends(cookie),
    user_session: SessionData = Depends(get_user_session),
):
    await delete_user_session(session_id)
    cookie.delete_from_response(response)

    return {"message": "Logged out"}








def get_user_by_id(db_session: Session, user_id: int):
    return db_session.exec(
        select(User).where(User.id == user_id)
    ).first()




def update_profile_pic(
        filename: str,
        db_session: Session,
        user_session: SessionData = Depends(get_user_session),
    ):
        
        user = get_user_by_id(db_session, user_session.user_id)

        if not user:
            return None

        user.profile_pic_url = filename

        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)

        return user



@router.get("/debug-update")
def debug(db: Session = Depends(get_db_session)):
    user = db.exec(select(User).where(User.id == 10)).first()

    user.profile_pic_url = "dog_user_10.png"

    db.commit()

    return {"ok": True}