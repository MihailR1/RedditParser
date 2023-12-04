from fastapi import APIRouter

from app.reddit.redit_app import reddit
from app.schemas import SubbReditSchema

router = APIRouter(
    prefix="/subbredits",
    tags=["Получить саббредиты"],
)


@router.get('/')
async def popular_subbredits(
        subbreddit_limit: int = 150) -> list[SubbReditSchema]:

    popular_subbredits: list[SubbReditSchema] = reddit.get_list_of_popular_subreddits(
        limit=subbreddit_limit
    )
    return popular_subbredits
