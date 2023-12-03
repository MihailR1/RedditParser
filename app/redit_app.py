import dataclasses

import praw

from app.config import settings
from app.mixins import (
    ConvertSchemasMixin,
    CountMixins,
    FilterPostMixin,
    GetSubbreditsMixin,
    OtherMixins,
)
from app.schemas import RedditCommentSchema, RedditPostSchema, SubbReditSchema


@dataclasses.dataclass(slots=True)
class Reddit(ConvertSchemasMixin, FilterPostMixin, GetSubbreditsMixin, CountMixins, OtherMixins):
    reddit: praw.Reddit = praw.Reddit(
        client_id=settings.REDDIT_CLIENT_ID,
        client_secret=settings.REDDIT_CLIENT_SECRET_KEY,
        redirect_uri=settings.REDDIT_REDIRECT_URI,
        user_agent=settings.REDDIT_USER_AGENT,
    )

    def get_list_of_popular_subreddits(self) -> list[SubbReditSchema]:
        reddits_iterator = self.reddit.subreddits.popular()
        subbredits_parsed_to_schema = self.convert_subreddits_to_schema(reddits_iterator)
        return subbredits_parsed_to_schema

    def grab_hot_posts_from_subbredid(self, subbredid: SubbReditSchema, limit=200) -> list[RedditPostSchema]:
        top_posts = self.reddit.subreddit(subbredid.name).hot(limit=limit)
        post_parsed_as_schema = self.convert_posts_to_schema(subbredid.name, top_posts)
        return post_parsed_as_schema

    def get_comments_from_post(self, post: praw.reddit.Submission, limit: int = 15) -> list[RedditCommentSchema] | None:
        top_comments = post.comments.list()[:limit]
        result_list = []
        for comment in top_comments:
            parsed_comment = self.convert_comment_to_schema(comment)
            if parsed_comment:
                result_list.append(parsed_comment)

        return result_list if result_list else None
