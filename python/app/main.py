from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, users, posts, comments

app = FastAPI()

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(posts.router)
app.include_router(comments.router)

app.add_middleware(
    CORSMiddleware, 
    allow_origins=["http://localhost:4200"],
    allow_credentials = True, 
    allow_methods = ["*"],
    allow_headers=["*"],
)