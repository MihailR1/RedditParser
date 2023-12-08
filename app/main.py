from fastapi import FastAPI

from app.routes.count import router as count_router
from app.routes.posts import router as posts_comments_router
from app.routes.subbredits import router as subreddit_router

app = FastAPI(
    title="Парсер Reddit",
)

app.include_router(subreddit_router)
app.include_router(posts_comments_router)
app.include_router(count_router)
