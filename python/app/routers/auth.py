from fastapi import APIRouter, Depends, HTTPException, Body
from sqlmodel import Session, select
from ..database.database import get_session
from ..models.models import User

router = APIRouter()
router = APIRouter(prefix="/auth")

def get_user_by_username(session: Session, username: str):
    return session.exec(
        select(User).where(User.username == username)
    ).first()

def get_user_by_email(session: Session, email: str):
    return session.exec(
        select(User).where(User.email == email)
    ).first()


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
def check_username(
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
    existing_user = get_user_by_username(
        session,
        username
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username already taken"
        )

    new_user = User(
        username=username,
        email=email,
        password_hash=password  # hash later!
    )

    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return {
        "message": "User created",
        "user_id": new_user.id
    }