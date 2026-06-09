from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, home

app = FastAPI()

app.include_router(auth.router)
#app.include_router(home.router)

app.add_middleware(
    CORSMiddleware, 
    allow_origins=["http://localhost:4200"],
    allow_credentials = True, 
    allow_methods = ["*"],
    allow_headers=["*"],
)