from fastapi import APIRouter, Depends, HTTPException
from ..core.sessions import SessionData, get_user_session
from ..core.uploads import get_user_profile_picture

router = APIRouter()
router = APIRouter(prefix="/users")


# GET endpoint for fetching profile pictures from the backend uploads folder
# Users must be logged in in order to be able to see profile pictures  
@router.get("/profile-picture/{filename}")
async def get_profile_picture(
    filename: str,
    user_session: SessionData = Depends(get_user_session),
):
    return get_user_profile_picture(filename)