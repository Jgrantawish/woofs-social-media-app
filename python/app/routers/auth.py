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