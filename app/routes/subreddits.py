from fastapi import APIRouter

from app.reddit.redit_app import reddit
from app.schemas import SubredditSchema

router = APIRouter(
    prefix="/subreddits",
    tags=["Получить сабреддиты"],
)


@router.get('/')
async def popular_subreddits(
        subreddit_limit: int = 150) -> list[SubredditSchema]:

    popular_subreddits: list[SubredditSchema] = reddit.get_list_of_popular_subreddits(
        limit=subreddit_limit
    )
    return popular_subreddits
