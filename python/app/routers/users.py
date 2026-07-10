from fastapi import APIRouter, Depends, HTTPException
from ..core.sessions import SessionData, get_user_session
from ..database.database import get_db_session
from ..core.uploads import get_user_profile_picture
from ..models.models import User
from ..models.responses import UserResponse
from sqlmodel import Session, select, delete
from typing import Optional


router = APIRouter(prefix="/users")

# Convert ORM object into UserResponse schema
def to_user_response(user: User) -> UserResponse:
    return UserResponse(
        id=user.id,
        username=user.username,
        profile_pic_url=user.profile_pic_url
    )


# GET endpoint for fetching profile pictures from the backend uploads folder
# Users must be logged in in order to be able to see profile pictures  
@router.get("/profile-pictures/{filename}")
async def get_profile_picture(
    filename: str,
    user_session: SessionData = Depends(get_user_session),
):
    return get_user_profile_picture(filename)


# GET endpoint to search users by thier usernames
@router.get("/search")
def search_users(
    search_text: Optional[str] = None,
    user_session: SessionData = Depends(get_user_session),
    db_session: Session = Depends(get_db_session)
):
    statement = select(User)

    if search_text:
        statement = statement.where(
            User.username.ilike(f"%{search_text}%")
        )

    results = db_session.exec(statement).all()

    # Convert each db row into the response schema before sending it to the front end 
    return [
        to_user_response(user) for user in results
    ]