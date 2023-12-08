import prawcore
import pytest

from app.exceptions import WrongsubredditName
from app.reddit.redit_app import reddit_posts


async def test__RedditPosts__exceptions():
    with pytest.raises(prawcore.exceptions.Redirect):
        assert reddit_posts.grab_top_posts_from_subbredid_by_name('Okek392j12')
