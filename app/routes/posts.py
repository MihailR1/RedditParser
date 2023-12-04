from fastapi import APIRouter

from app.reddit.redit_app import reddit_posts
from app.schemas import RedditPostSchema

router = APIRouter(
    prefix='/posts',
    tags=['Посты и комментарии'],
)


@router.get('/{subbredit_name}')
async def posts_from_subbreditd_by_name(
        subbredit_name: str,
        posts_limit: int = 200,
        post_for_days: int = 3):

    """Получить именя популярных саббреддитов по роуту: /subbredits/
    Или ввести свое имя по шаблону 'AskReddit'
    **На больших лимитах (200) - парсить будет долго 3-5 минуты,
    но соберет за все 3 дня"""

    posts_in_schema: list[RedditPostSchema] = reddit_posts.grab_hot_posts_from_subbredid_by_name(
        subbredit_name, posts_limit
    )
    filted_posts_by_days: list[RedditPostSchema] = reddit_posts.filter_posts_by_date_range(
        posts_in_schema, days_behind=post_for_days
    )
    return filted_posts_by_days
