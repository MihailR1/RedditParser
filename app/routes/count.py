import typing

from fastapi import APIRouter

from app.enums import PopularTextTypes
from app.reddit.redit_app import reddit_posts
from app.routes.posts import posts_from_subreddits_by_name
from app.schemas import RedditPostSchema

router = APIRouter(
    prefix='/count',
    tags=['Популярные посты и комменты']
)


@router.get('/{subreddit_name}')
async def popular_posts(
        subreddit_name: str,
        posts_limit: int = 200,
        post_for_days: int = 3,
        limit_of_user_to_show: int = 10):

    """На входе: имя сабреддита, на выходе json с популярными постами,
    отсортированными по убыванию.
    Получить имена популярных сабреддитов по роуту: /subreddits/
    Или ввести любое имя по шаблону 'AskReddit'
    **На больших лимитах (200) - парсить будет долго 3-5 минуты,
    но соберет за все 3 дня"""

    filtered_posts_from_subreddit: list[RedditPostSchema] | None = await posts_from_subreddits_by_name(
        subreddit_name, posts_limit, post_for_days
    )

    if filtered_posts_from_subreddit:
        count_user_posts: list[tuple[str, int]] = reddit_posts.count_author_posts(
            filtered_posts_from_subreddit
        )

        represent_posts: typing.Mapping[str, str] = reddit_posts.presentation_poplar_comments_and_posts(
            PopularTextTypes.post, count_user_posts, limit_of_user_to_show
        )

        return represent_posts

    return None


@router.get('/comments/{subreddit_name}')
async def popular_comments(
        subreddit_name: str,
        posts_limit: int = 200,
        post_for_days: int = 3,
        limit_of_user_to_show: int = 10):

    """На входе: имя сабреддита, на выходе json с популярными постами,
        отсортированными по убыванию.
        Получить имена популярных сабреддитов по роуту: /subreddits/
        Или ввести любое имя по шаблону 'AskReddit'
        **На больших лимитах (200) - парсить будет долго 3-5 минуты,
        но соберет за все 3 дня"""

    filtered_posts_from_subreddit: list[RedditPostSchema] | None = await posts_from_subreddits_by_name(
        subreddit_name, posts_limit, post_for_days
    )

    if filtered_posts_from_subreddit:
        count_user_comments: list[tuple[str, int]] = reddit_posts.count_comments_by_user(
            filtered_posts_from_subreddit
        )

        represent_comments: typing.Mapping[str, str] = reddit_posts.presentation_poplar_comments_and_posts(
            PopularTextTypes.comment, count_user_comments, limit_of_user_to_show
        )

        return represent_comments

    return None
