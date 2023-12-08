import dataclasses
import datetime
from typing import Iterator

import praw
import prawcore

from app.config import settings
from app.enums import TimeFilterPosts
from app.exceptions import ConnectionProblemToReddit, WrongsubredditName
from app.reddit.mixins import ConvertSchemasMixin, CountMixins
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

        subreddits_parsed_to_schema: list[SubredditSchema] = self.convert_subreddits_to_schema(
            reddits_iterator)

        return subreddits_parsed_to_schema


@dataclasses.dataclass(slots=True)
class RedditPosts(Reddit, CountMixins):
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
            """Ошибки из библиотеки praw почему-то не отрабатывают"""
            raise WrongsubredditName

        post_parsed_as_schema: list[RedditPostSchema] = self.convert_posts_to_schema(subbredid, top_posts)

        return post_parsed_as_schema

    @staticmethod
    def filter_posts_by_date_range(
            posts: list[RedditPostSchema],
            day_start: datetime.datetime = datetime.datetime.utcnow(),
            days_behind: int = 3) -> list[RedditPostSchema] | None:

        datetime_behind: datetime.datetime = day_start - datetime.timedelta(days=days_behind)
        filtered_posts: Iterator = filter(lambda post: post.created_at_utc >= datetime_behind, posts)
        filter_posts: list = list(filtered_posts)

        return filter_posts if filter_posts else None


reddit = Reddit()
reddit_posts = RedditPosts()
