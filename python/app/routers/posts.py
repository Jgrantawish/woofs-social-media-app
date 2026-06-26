from fastapi import APIRouter, Depends
from ..core.sessions import SessionData, get_user_session

router = APIRouter()
router = APIRouter(prefix="/posts")

@router.get("/")
def get_posts(user_session: SessionData = Depends(get_user_session)):
    return user_session