from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from ..core.sessions import SessionData, get_user_session
from ..core.uploads import upload_post_image
from sqlmodel import Session, select
from ..models.models import Post
from ..database.database import get_db_session
from datetime import datetime
from typing import Optional


router = APIRouter()
router = APIRouter(prefix="/posts")

@router.get("/")
def get_posts(user_session: SessionData = Depends(get_user_session)):
    return user_session



# POST endpoint for posting a new social media post by the logged in user
@router.post("/new")
async def create_new_post(
    image: Optional[UploadFile] = File(None),
    content: Optional[str] = Form(None),
    user_session: SessionData = Depends(get_user_session),
    db_session: Session = Depends(get_db_session)
):
    # Check that the post is not completely empty
    if not image and not (content and content.strip()):
        raise HTTPException(
            status_code=400,
            detail="Post must contain an image or text"
        )
    
    image_url = None

    # If an image file was uploaded as part of the post, save it to the uploads folder
    if image:
        image_url = await upload_post_image(image)

    new_post = Post(
        user_id = user_session.user_id,
        picture_url= image_url,
        content=content.strip() if content and content.strip() else None,
        created_date=datetime.now()
    )

    db_session.add(new_post)
    db_session.commit()
    db_session.refresh(new_post)

    return {"message": "Post created"}