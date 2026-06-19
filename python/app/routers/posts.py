from fastapi import APIRouter, Depends, HTTPException, Body
from ..core.sessions import session_verifier, SessionData

router = APIRouter()
router = APIRouter(prefix="/posts")

@router.get("/")
async def get_posts(
    user_session: SessionData = Depends(session_verifier)
):
    return user_session
