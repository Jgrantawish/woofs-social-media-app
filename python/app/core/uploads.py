from fastapi import UploadFile, HTTPException
from fastapi.responses import FileResponse
from pathlib import Path
from uuid import uuid4
import shutil

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

# Take the file uploaded and store it in the uploads directory
# Return the filename to be stored in the db 
async def upload_post_image(file: UploadFile) -> str:
    # Check that an image was actually uploaded
    if not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail="File must be an image"
        )
    
    UPLOAD_DIR = Path("uploads/post_images")
    # If the directory doesn't already exist, create it
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

    # Retain the image file type
    extension = Path(file.filename).suffix
    # Create a unique filename for the image
    filename = f"{uuid4()}{extension}"

    file_path = UPLOAD_DIR / filename

    try:
        # Open the file in binary write mode and copy the uploaded file into it
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except OSError as e:
        raise HTTPException(
            status_code=500,
            detail="Failed to save uploaded file"
        ) from e
    finally:
        # Close the file once finished
        await file.close()

    return str(filename)