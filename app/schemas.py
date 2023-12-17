import datetime
from typing import Any

from pydantic import AliasPath, BaseModel, Field, computed_field

from app.config import settings


class SubredditSchema(BaseModel):
    url: str = Field(exclude=True, validation_alias=AliasPath('url'))

    @computed_field
    @property
    def full_url(self) -> str:
        return settings.REDDIT_BASE_URL + self.url

    @computed_field
    @property
    def name(self) -> str:
        *_, name, _ = self.url.split('/')
        return name


class RedditPostSchema(BaseModel):
    title: str = Field(validation_alias=AliasPath('title'))
    author_obj: Any = Field(exclude=True, validation_alias=AliasPath('author'))
    author_id: str = Field(validation_alias=AliasPath('author_fullname'))
    subreddit_obj: Any = Field(exclude=True, validation_alias=AliasPath('subreddit'))
    created_at_utc: datetime.datetime = Field(default_factory=datetime.datetime.fromtimestamp,
                                              validation_alias=AliasPath('created_utc'))
    url: str = Field(exclude=True, validation_alias=AliasPath('permalink'))
    number_of_comments: int = Field(validation_alias=AliasPath('num_comments'))
    score: int = Field(validation_alias=AliasPath('score'))
    ups: int = Field(validation_alias=AliasPath('ups'))
    comments: list['RedditCommentSchema'] | None

    @computed_field
    @property
    def full_url(self) -> str:
        return settings.REDDIT_BASE_URL + self.url

    @computed_field
    @property
    def author(self) -> str:
        return self.author_obj.name

    @computed_field
    @property
    def subreddit_name(self) -> str:
        return self.subreddit_obj.display_name


class RedditCommentSchema(BaseModel):
    author_obj: Any = Field(exclude=True, validation_alias=AliasPath('author'))
    author_id: str = Field(validation_alias=AliasPath('author_fullname'))
    datetime_post: datetime.datetime = Field(default_factory=datetime.datetime.fromtimestamp,
                                             validation_alias=AliasPath('created_utc'))
    score: int = Field(validation_alias=AliasPath('score'))
    comment_text: str = Field(validation_alias=AliasPath('body'))
    url: str = Field(exclude=True, validation_alias=AliasPath('permalink'))

    @computed_field
    @property
    def link(self) -> str:
        return settings.REDDIT_BASE_URL + self.url

    @computed_field
    @property
    def author(self) -> str:
        return self.author_obj.name
