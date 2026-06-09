from fastapi import FastAPI
from app.routers import auth, home

app = FastAPI()

app.include_router(auth.router)
#app.include_router(home.router)

