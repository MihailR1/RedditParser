import pytest

from app.routes.subbredits import popular_subbredits


@pytest.mark.parametrize('limit', [10, -10, 150, 300, 800])
async def test__popular_subbredits__different_limits(limit):
    assert len(await popular_subbredits(limit)) == limit
