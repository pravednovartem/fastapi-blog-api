from fastapi import FastAPI

from .database import Base, engine
from .routers import comments, posts

Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastAPI Blog")

app.include_router(posts.router)
app.include_router(comments.router)


@app.get("/")
def root():
    return {"message": "FastAPI blog is running"}