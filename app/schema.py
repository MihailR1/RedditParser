import datetime

from pydantic import BaseModel


class SubbReditSchema(BaseModel):
    index: int
    name: str
    full_url: str


class RedditPostSchema(BaseModel):
    title: str
    author: str
    author_id: str
    subbreddit_name: str
    created_at_utc: datetime.datetime
    full_url: str
    number_of_comments: int
    score: int
    ups: int
