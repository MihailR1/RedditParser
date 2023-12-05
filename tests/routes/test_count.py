import pytest

from app.routes.count import popular_posts, popular_comments


@pytest.mark.parametrize(
    'subbredit_name, posts_limit, limit_of_user_to_show',
    [
        ('AskReddit', 5, 10),
        ('Home', -2, 15),
        ('/videos', 15, 3),
        ('GTA6/', 10, 2),
        ('/me_irl/', 20, 15)
    ]
)
async def test__popular_posts__different_kwargs(subbredit_name, posts_limit, limit_of_user_to_show):
    result = await popular_posts(
        subbredit_name=subbredit_name,
        posts_limit=posts_limit,
        limit_of_user_to_show=limit_of_user_to_show
    )

    assert isinstance(result, dict)
    assert 'Номер 1' in result.keys()
    assert len(result) <= limit_of_user_to_show


@pytest.mark.parametrize(
    'subbredit_name, posts_limit, limit_of_user_to_show',
    [
        ('AskReddit', 5, 10),
        ('Home', -2, 15),
        ('/videos', 15, 3),
        ('GTA6/', 10, 2),
        ('/me_irl/', 10, 15)
    ]
)
async def test__popular_comments__different_kwargs(subbredit_name, posts_limit, limit_of_user_to_show):
    result = await popular_comments(
        subbredit_name=subbredit_name,
        posts_limit=posts_limit,
        limit_of_user_to_show=limit_of_user_to_show
    )

    assert isinstance(result, dict)
    assert 'Номер 1' in result.keys()
    assert len(result) <= limit_of_user_to_show
