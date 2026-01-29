from fastapi import FastAPI
from .routers import posts, users, auth, votes
from contextlib import asynccontextmanager
from . import database_model
from .database import engine

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     database_model.Base.metadata.create_all(bind=engine)
#     yield

# app = FastAPI(lifespan=lifespan)
app = FastAPI()

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(votes.router)

@app.get('/')
def hello():
    return {"Message": "Hello User of new reload"}
