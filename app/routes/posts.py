from fastapi import APIRouter

from app.enums import TimeFilterPosts
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

    time_filter: TimeFilterPosts = TimeFilterPosts.week

    if 7 < post_for_days <= 30:
        time_filter = TimeFilterPosts.month
    elif post_for_days >= 31:
        time_filter = TimeFilterPosts.year
    elif post_for_days > 365:
        time_filter = TimeFilterPosts.all

    posts_in_schema: list[RedditPostSchema] = reddit_posts.grab_top_posts_from_subbredid_by_name(
        subbredit_name, posts_limit, time_filter=time_filter
    )

    filted_posts_by_days: list[RedditPostSchema] | None = reddit_posts.filter_posts_by_date_range(
        posts_in_schema, days_behind=post_for_days
    )

    return filted_posts_by_days
