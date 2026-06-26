from fastapi_sessions.backends.implementations import InMemoryBackend
from fastapi_sessions.frontends.implementations import SessionCookie, CookieParameters
from pydantic import BaseModel
from ..config import settings
from uuid import UUID, uuid4
from fastapi import HTTPException, Depends

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
async def create_user_session(user_id: int, username: str) -> UUID:
    session_id = uuid4()
    user_data = SessionData(user_id=user_id,username=username)
    await backend.create(session_id, user_data)
    return session_id

# Extract the session ID from the client's cookie
# Use the session ID to look up the session data associated with it
async def get_user_session(session_id: UUID = Depends(cookie)) -> SessionData:
    session = await backend.read(session_id)

    # If no session exists for the session ID then the user is not authenticated
    if session is None:
        raise HTTPException(status_code=403, detail="Invalid session")

    return session

# Remove the session from backend memory for the specified session ID
async def delete_user_session(session_id: UUID) -> None:
    await backend.delete(session_id)
