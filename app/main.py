from fastapi import FastAPI

from app.routes.count import router as count_router
from app.routes.posts import router as posts_comments_router
from app.routes.subbredits import router as subbredit_router

app = FastAPI(
    title="Парсер Reddit",
)

app.include_router(subbredit_router)
app.include_router(posts_comments_router)
app.include_router(count_router)
