import pytest

from app.routes.subreddits import popular_subreddits


@pytest.mark.parametrize('limit', [10, -10, 150, 300, 800])
async def test__popular_subreddits__different_limits(limit):
    assert len(await popular_subreddits(limit)) == limit
