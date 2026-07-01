from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from ..core.sessions import SessionData, get_user_session
from pathlib import Path

router = APIRouter()
router = APIRouter(prefix="/uploads")

# GET endpoint for fetching profile pictures from the backend uploads folder
# Users must be logged in in order to be able to see profile pictures  
@router.get("/profile-picture/{filename}")
async def get_profile_picture(
    filename: str,
    user_session: SessionData = Depends(get_user_session),
):
    UPLOAD_DIR = Path("uploads/profile_pictures")
    file_path = UPLOAD_DIR / filename

    if not file_path.exists():
        raise HTTPException(status_code=404)

    return FileResponse(file_path)

