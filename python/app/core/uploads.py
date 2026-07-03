from fastapi import UploadFile, HTTPException
from fastapi.responses import FileResponse
from pathlib import Path
# Use the specified filename to fetch a profile picture from the uploads folder
def get_user_profile_picture(filename: str):
    UPLOAD_DIR = Path("uploads/profile_pictures")
    file_path = UPLOAD_DIR / filename

    if not file_path.exists():
        raise HTTPException(
            status_code=404, 
            detail="File does not exist"
        )

    return FileResponse(file_path)

