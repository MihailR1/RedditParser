import datetime

import pytest

from app.routes.posts import posts_from_subbreditd_by_name
from app.schemas import RedditPostSchema


@pytest.mark.parametrize(
    'subbredit_name, posts_limit, post_for_days',
    [
        ('AskReddit', 5, 3),
        ('Home', -2, 3),
        ('Home', 2, -3),
        ('/videos', 15, 3),
        ('GTA6/', 50, 5),
        ('/me_irl/', 10, 3)
    ],
    ids=['success', 'fail', 'fail', 'success', 'success', 'success']
)
async def test__posts_from_subbreditd_by_name__different_kwargs(
        subbredit_name,
        posts_limit,
        post_for_days):

    date_with_days_behind = datetime.datetime.utcnow() - datetime.timedelta(days=post_for_days)

    result = await posts_from_subbreditd_by_name(subbredit_name, posts_limit, post_for_days)
    result_schema: RedditPostSchema = result[0]

    assert result_schema.subbreddit_name == subbredit_name
    assert result_schema.created_at_utc >= date_with_days_behind
    assert len(result) <= posts_limit
