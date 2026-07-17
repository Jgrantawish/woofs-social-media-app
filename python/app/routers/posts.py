from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Body
from ..core.sessions import SessionData, get_user_session
from ..core.uploads import upload_post_image, get_post_image, delete_post_image
from sqlmodel import Session, select, delete
from sqlalchemy.orm import selectinload
from sqlalchemy import func, exists
from ..models.models import Post, Comment, Like
from ..models.responses import PostResponse
from ..database.database import get_db_session
from datetime import datetime
from typing import Optional


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
    searched_user_id: Optional[int] = None,
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
            .correlate(Post)
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

    # If they have searched for a user, filter to only posts created by that user  
    if searched_user_id is not None:
        statement = statement.where(Post.user_id == searched_user_id)

    # Execute query (returns rows in the form: Post, like_count, has_liked)
    results = db_session.exec(statement).all()

    # Convert each db row into the response schema before sending it to the front end 
    return [
        to_post_response(post, user_session.user_id, like_count, has_liked, comment_count)
        for post, like_count, has_liked, comment_count in results
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
    MAX_CONTENT_LENGTH = 280
    content = content.strip() if content else None
    
    # Check that the post is not completely empty
    if not image and not content:
        raise HTTPException(
            status_code=400,
            detail="Post must contain an image or text"
        )
    
    # If content was uploaded, check it is not longer than max character length
    if content and len(content) > MAX_CONTENT_LENGTH:
        raise HTTPException(
            status_code=400,
            detail=f"Content must be less than {MAX_CONTENT_LENGTH} characters"
        )
    

    image_url = None

    # If an image file was uploaded as part of the post, save it to the uploads folder
    if image:
        image_url = await upload_post_image(image)

    new_post = Post(
        user_id = user_session.user_id,
        picture_url= image_url,
        content=content,
        created_date=datetime.now()
    )

    db_session.add(new_post)
    db_session.commit()
    db_session.refresh(new_post)

    return {"message": "Post created"}



# PUT endpoint for editing a social media post by the logged in user
@router.put("/edit")
async def edit_post(
    post_id: int = Form(),
    remove_original_image: bool = Form(False),
    image: Optional[UploadFile] = File(None),
    content: Optional[str] = Form(None),
    user_session: SessionData = Depends(get_user_session),
    db_session: Session = Depends(get_db_session)
):
    MAX_CONTENT_LENGTH = 280
    content = content.strip() if content else None

    post = db_session.get(Post, post_id)

    # Check post exists
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    # Check ownership
    if post.user_id != user_session.user_id:
        raise HTTPException(status_code=403, detail="Not allowed")
    
    original_image_url = post.picture_url

    # Check that the edited post is not completely empty
    if not image and not content and (remove_original_image or not original_image_url):
        raise HTTPException(
            status_code=400,
            detail="Post must contain an image or text"
        )
    
    # Check that any content is still no longer than max character length
    if content and len(content) > MAX_CONTENT_LENGTH:
        raise HTTPException(
            status_code=400,
            detail=f"Content must be less than {MAX_CONTENT_LENGTH} characters"
        )
    
    post.content = content

    # If a the original post image was removed or replaced, remove it from the uploads folder and the post db record
    if original_image_url and remove_original_image:
        delete_post_image(original_image_url)
        post.picture_url = None


    # If a different image file was uploaded as part of the edit, save it to the uploads folder and the post db record
    updated_image_url = None
    if image:
        updated_image_url = await upload_post_image(image)
        post.picture_url = updated_image_url

    post.last_updated = datetime.now()

    db_session.commit()
    db_session.refresh(post)

    return {"message": "Post updated"}


# DELETE endpoint deleting a specified post
@router.delete("/delete")
def delete_post(
    post_id: int = Body(...),
    user_session: SessionData = Depends(get_user_session),
    db_session: Session = Depends(get_db_session),
):
    post = db_session.get(Post, post_id)

    # Check post exists
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    # Check ownership
    if post.user_id != user_session.user_id:
        raise HTTPException(status_code=403, detail="Not allowed")
    
    image_url = post.picture_url

    db_session.delete(post)
    db_session.commit()

    # If the deleted post contained an image, remove it from our uploads folder
    if image_url:
        delete_post_image(image_url)

    return {"message": "Post deleted"}


# POST endpoint for liking a specified post
@router.post("/add-like")
async def add_like(
    post_id: int = Body(..., embed=True),
    user_session: SessionData = Depends(get_user_session),
    db_session: Session = Depends(get_db_session)
):
    # Check that the logged in user has not already liked this post
    existing_like = db_session.exec(
        select(Like).where(
            Like.post_id == post_id,
            Like.user_id == user_session.user_id,
        )
    ).first()

    if existing_like:
        raise HTTPException(
            status_code=400,
            detail="You cannot like a post more than once"
        )

    new_like = Like(
        post_id=post_id,
        user_id=user_session.user_id,
    )

    db_session.add(new_like)
    db_session.commit()
    db_session.refresh(new_like)

    return {"message": "Like added to post"}    


# DELETE endpoint for removing a like from a post
@router.delete("/remove-like")
async def remove_like(
    post_id: int = Body(...),
    user_session: SessionData = Depends(get_user_session),
    db_session: Session = Depends(get_db_session)
):
    statement = (
        delete(Like)
        .where(
            Like.post_id == post_id,
            Like.user_id == user_session.user_id,
        )
    )

    result = db_session.exec(statement)
    db_session.commit()

    # If no like was actually deleted from the table, throw an error so that front end does not change the GUI 
    if result.rowcount == 0:
        raise HTTPException(
            status_code=404, 
            detail="You cannot unlike a post more than once"
        )

    return {"message": "Like removed from post"}