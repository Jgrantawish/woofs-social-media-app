from fastapi import APIRouter, Depends, HTTPException
from ..core.sessions import SessionData, get_user_session
from ..database.database import get_db_session
from sqlmodel import Session, select
from sqlalchemy.orm import selectinload
from sqlalchemy import func, exists
from ..models.models import Comment
from ..models.responses import CommentResponse


router = APIRouter(prefix="/comments")


# Convert ORM objects into CommentResponse schema
def to_comment_response(comment: Comment, logged_in_user_id: int) -> CommentResponse:
    return CommentResponse(
        id=comment.id,
        content=comment.content,
        created_date=comment.created_date,
        last_updated=comment.last_updated,

        owner_username=comment.user.username,
        owner_profile_pic_url=comment.user.profile_pic_url,
        is_owner = comment.user_id == logged_in_user_id
    )


# GET endpoint for fetching the comments on a specified post
@router.get("/{post_id}")
async def get_comments(
    post_id: int,
    user_session: SessionData = Depends(get_user_session),
    db_session: Session = Depends(get_db_session)
):
    statement = (
        select(Comment)
        .where(Comment.post_id == post_id)
        .options(
            # Eager load the associated user data for the specified comment 
            selectinload(Comment.user)
        )
        .order_by(Comment.created_date)
    )

    results = db_session.exec(statement).all()

    # Convert each db row into the response schema before sending it to the front end 
    return [
        to_comment_response(comment, user_session.user_id) for comment in results
    ]



# POST endpoint for adding a comment to a post
