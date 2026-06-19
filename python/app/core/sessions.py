from fastapi_sessions.backends.implementations import InMemoryBackend
from fastapi_sessions.frontends.implementations import SessionCookie, CookieParameters
from fastapi_sessions.session_verifier import SessionVerifier as BaseSessionVerifier
from pydantic import BaseModel
from ..config import settings
from uuid import UUID, uuid4
from fastapi import HTTPException

# Store the username in the session
class SessionData(BaseModel):
    user_id: int
    username: str

# Create a session cookie (it uses UUID to identify the session)
cookie = SessionCookie(
    cookie_name="cookie",
    identifier="general_verifier",
    auto_error=True,
    secret_key=settings.SECRET_KEY,
    cookie_params=CookieParameters(
    secure=False, # Change to True in production so cookies are sent using https 
    httponly=True,
    samesite="lax" # help prevent against CSRF attacks
    )
)

# Store the session data in voilatile, server memory 
backend = InMemoryBackend[UUID, SessionData]()

# Create a session for the specified user
def create_user_session(user_id: int, username: str):
    session_id = uuid4()
    user_data = SessionData(user_id=user_id,username=username)
    backend.create(session_id, user_data)
    return session_id


