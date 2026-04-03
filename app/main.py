from fastapi import FastAPI

from .routers import categories, comments, locations, posts, users

app = FastAPI(title="FastAPI + Django SQLite")

app.include_router(categories.router)
app.include_router(locations.router)
app.include_router(users.router)
app.include_router(posts.router)
app.include_router(comments.router)


@app.get("/")
def root():
    return {"message": "FastAPI works with Django SQLite database"}
