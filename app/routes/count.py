import typing

from fastapi import APIRouter

from app.enums import PopularTextTypes
from app.reddit.redit_app import reddit_posts
from app.routes.posts import posts_from_subbreditd_by_name
from app.schemas import RedditPostSchema

router = APIRouter(
    prefix='/count',
    tags=['Популярные посты и комменты']
)


@router.get('/{subbredit_name}')
async def popular_posts(
        subbredit_name: str,
        posts_limit: int = 200,
        post_for_days: int = 3,
        limit_of_user_to_show: int = 10):

    """На входе: имя саббреддита, на выходе json с популярными постами,
    отсортированными по убыванию.
    Получить именя популярных саббреддитов по роуту: /subbredits/
    Или ввести свое имя по шаблону 'AskReddit'
    **На больших лимитах (200) - парсить будет долго 3-5 минуты,
    но соберет за все 3 дня"""

    filtered_posts_from_subbredit: list[RedditPostSchema] = await posts_from_subbreditd_by_name(
        subbredit_name, posts_limit, post_for_days
    )

    count_user_posts: list[tuple[str, int]] = reddit_posts.count_author_posts(
        filtered_posts_from_subbredit
    )

    represent_posts: typing.Mapping[str | str] = reddit_posts.presentation_poplar_comments_and_posts(
        PopularTextTypes.post, count_user_posts, limit_of_user_to_show
    )

    return represent_posts


@router.get('/comments/{subbredit_name}')
async def popular_comments(
        subbredit_name: str,
        posts_limit: int = 200,
        post_for_days: int = 3,
        limit_of_user_to_show: int = 10):
    """На входе: имя саббреддита, на выходе json с популярными постами,
        отсортированными по убыванию.
        Получить именя популярных саббреддитов по роуту: /subbredits/
        Или ввести свое имя по шаблону 'AskReddit'
        **На больших лимитах (200) - парсить будет долго 3-5 минуты,
        но соберет за все 3 дня"""

    filtered_posts_from_subbredit: list[RedditPostSchema] = await posts_from_subbreditd_by_name(
        subbredit_name, posts_limit, post_for_days
    )

    count_user_comments: list[tuple[str, int]] = reddit_posts.count_comments_by_user(
        filtered_posts_from_subbredit
    )

    represent_comments: typing.Mapping[str | str] = reddit_posts.presentation_poplar_comments_and_posts(
        PopularTextTypes.comment, count_user_comments, limit_of_user_to_show
    )

    return represent_comments
