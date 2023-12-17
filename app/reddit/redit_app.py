import dataclasses
from typing import Iterator

import praw
import prawcore

from app.config import settings
from app.enums import TimeFilterPosts
from app.exceptions import ConnectionProblemToReddit, WrongSubredditName
from app.reddit.mixins import ConvertSchemasMixin, UtilsMixins
from app.schemas import RedditPostSchema, SubredditSchema


@dataclasses.dataclass(slots=True)
class Reddit(ConvertSchemasMixin):
    reddit: praw.Reddit = praw.Reddit(
        client_id=settings.REDDIT_CLIENT_ID,
        client_secret=settings.REDDIT_CLIENT_SECRET_KEY,
        redirect_uri=settings.REDDIT_REDIRECT_URI,
        user_agent=settings.REDDIT_USER_AGENT,
    )

    def get_list_of_popular_subreddits(self, limit: int = 200) -> list[SubredditSchema]:

        try:
            reddits_iterator: Iterator[praw.reddit.Subreddit] = self.reddit.subreddits.popular(limit=limit)
        except prawcore.exceptions.PrawcoreException:
            raise ConnectionProblemToReddit

        subreddits_parsed_to_schema: list[SubredditSchema] = self.validate_list_to_schema(
            reddits_iterator, SubredditSchema)

        return subreddits_parsed_to_schema


@dataclasses.dataclass(slots=True)
class RedditPosts(Reddit, UtilsMixins):
    def grab_top_posts_from_subbredid_by_name(
            self,
            subbredid: str,
            limit: int = 200,
            time_filter: TimeFilterPosts = TimeFilterPosts.week) -> list[RedditPostSchema]:

        try:
            top_posts: Iterator[praw.reddit.Subreddit] = self.reddit.subreddit(subbredid).top(
                limit=limit,
                time_filter=time_filter.value
            )
        except prawcore.exceptions.Redirect:
            raise WrongSubredditName

        post_parsed_as_schema: list[RedditPostSchema] = self.convert_posts_to_schema(top_posts)

        return post_parsed_as_schema


reddit = Reddit()
reddit_posts = RedditPosts()
