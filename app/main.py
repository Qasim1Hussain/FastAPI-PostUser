from fastapi import FastAPI
from .routers import posts, users, auth, votes

from . import database_model
from .database import engine
database_model.Base.metadata.create_all(bind=engine)


app = FastAPI()

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(votes.router)