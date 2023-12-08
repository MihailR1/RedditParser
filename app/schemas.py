import datetime

from pydantic import BaseModel


class SubredditSchema(BaseModel):
    index: int
    name: str
    full_url: str


class RedditPostSchema(BaseModel):
    title: str
    author: str
    author_id: str
    subreddit_name: str
    created_at_utc: datetime.datetime
    full_url: str
    number_of_comments: int
    score: int
    ups: int
    comments: list['RedditCommentSchema'] | None


class RedditCommentSchema(BaseModel):
    author: str
    author_id: str
    datetime_post: datetime.datetime
    score: int
    comment_text: str
    link: str
