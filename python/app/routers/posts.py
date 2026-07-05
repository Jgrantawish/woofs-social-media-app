from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from ..core.sessions import SessionData, get_user_session
from ..core.uploads import upload_post_image, get_post_image
from sqlmodel import Session, select
from sqlalchemy.orm import selectinload
from sqlalchemy import func, exists
from ..models.models import Post, Comment, Like
from ..models.responses import PostResponse
from ..database.database import get_db_session
from datetime import datetime
from typing import Optional


router = APIRouter()
router = APIRouter(prefix="/posts")


# Convert ORM objects and precomputed metadata into PostResponse schema
def to_post_response(post: Post, logged_in_user_id: int, like_count, has_liked, comment_count) -> PostResponse:
    return PostResponse(
        id=post.id,
        picture_url=post.picture_url,
        content=post.content,
        created_date=post.created_date,
        last_updated=post.last_updated,

        owner_username=post.user.username,
        owner_profile_pic_url=post.user.profile_pic_url,
        is_owner = post.user_id == logged_in_user_id,

        like_count=like_count,
        has_liked=has_liked,

        comment_count=comment_count
    )

# GET endpoint for fetching all social metia posts (and their associated metadata)
@router.get("/", response_model=list[PostResponse])
def get_posts(
    user_session: SessionData = Depends(get_user_session),
    db_session: Session = Depends(get_db_session)
):
    # Subquery that returns the number of likes for each post
    # This avoids loading large amounts of likes data into Python
    like_count_subquery = (
        select(func.count(Like.user_id))
        .where(Like.post_id == Post.id)
        .scalar_subquery()
    )

    # Subquery that returns boolean for whether the logged in user has liked the post
    has_liked_subquery = (
        select(
            exists().where(
                Like.post_id == Post.id,
                Like.user_id == user_session.user_id
            )
        ).scalar_subquery()
    )

    # Subquery that returns the total number of comments on a post
    comment_count_subquery = (
        select(func.count(Comment.id))
        .where(Comment.post_id == Post.id)
        .scalar_subquery()
    )

    statement = (
        select(
            Post,
            # Attach computed like count, comment count and liked boolean flag as extra selected columns
            like_count_subquery.label("like_count"),
            has_liked_subquery.label("has_liked"),
            comment_count_subquery.label("comment_count")
            )
        .options(
            # Eager load the related user for each post (avoids extra queries)
            selectinload(Post.user)
        )
        # Sort posts so that the newest posts appear first
        .order_by(Post.created_date.desc())
    )

    # Execute query (returns rows in the form: Post, like_count, has_liked)
    results = db_session.exec(statement).all()

    # Convert each db row into the response schema before sending it to the front end 
    return [
        to_post_response(post, user_session.user_id, like_count, has_liked)
        for post, like_count, has_liked in results
    ]


# GET endpoint for fetching pictures associated with posts from the backend uploads folder
@router.get("/images/{filename}")
async def get_picture(
    filename: str,
    user_session: SessionData = Depends(get_user_session),
):
    return get_post_image(filename)


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