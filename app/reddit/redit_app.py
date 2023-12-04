import dataclasses
from typing import Iterator

import praw

from app.config import settings
from app.exceptions import ConnectionProblemToReddit, WrongSubbredditName
from app.reddit.mixins import ConvertSchemasMixin, CountMixins, FilterPostMixin
from app.schemas import RedditCommentSchema, RedditPostSchema, SubbReditSchema


@dataclasses.dataclass(slots=True)
class Reddit(ConvertSchemasMixin):
    reddit: praw.Reddit = praw.Reddit(
        client_id=settings.REDDIT_CLIENT_ID,
        client_secret=settings.REDDIT_CLIENT_SECRET_KEY,
        redirect_uri=settings.REDDIT_REDIRECT_URI,
        user_agent=settings.REDDIT_USER_AGENT,
    )

    def get_list_of_popular_subreddits(self, limit: int = 200) -> list[SubbReditSchema]:
        try:
            reddits_iterator: list[praw.reddit.Subreddit] = self.reddit.subreddits.popular(limit=limit)
        except Exception:
            """Exceptions из библиотеки praw почему-то не отрабатывают"""
            raise ConnectionProblemToReddit

        subbredits_parsed_to_schema: list[SubbReditSchema] = self.convert_subreddits_to_schema(reddits_iterator)

        return subbredits_parsed_to_schema


@dataclasses.dataclass(slots=True)
class RedditPosts(Reddit, FilterPostMixin, CountMixins):
    def grab_hot_posts_from_subbredid_by_name(
            self,
            subbredid: str,
            limit=200) -> list[RedditPostSchema]:

        try:
            top_posts: Iterator[praw.reddit.Subreddit] = self.reddit.subreddit(subbredid).hot(limit=limit)
        except Exception:
            """Ошибки из библиотеки praw почему-то не отрабатывают"""
            raise WrongSubbredditName

        post_parsed_as_schema: list[RedditPostSchema] = self.convert_posts_to_schema(subbredid, top_posts)

        return post_parsed_as_schema

    def grab_hot_posts_from_subbredid_schema(
            self,
            subbredid: SubbReditSchema,
            limit=200) -> list[RedditPostSchema]:

        top_posts: list[RedditPostSchema] = self.grab_hot_posts_from_subbredid_by_name(
            subbredid.name, limit
        )

        return top_posts

    def get_comments_from_post(
            self,
            post: praw.reddit.Submission,
            limit: int = 15) -> list[RedditCommentSchema] | None:

        top_comments: list[praw.reddit.Comment] = post.comments.list()[:limit]
        result_list: list = []

        for comment in top_comments:
            parsed_comment: dict[str, str | int] | None = self.convert_comment_to_schema(comment)
            if parsed_comment:
                result_list.append(parsed_comment)

        return result_list if result_list else None


reddit = Reddit()
reddit_posts = RedditPosts()
