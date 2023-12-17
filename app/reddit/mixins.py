import datetime
from typing import Iterator, TypeVar, Generic

import praw
import pydantic
import pytz as pytz

from app.enums import PopularTextTypes
from app.schemas import RedditCommentSchema, RedditPostSchema


class ConvertSchemasMixin:
    _SchemaType = TypeVar('_SchemaType', bound=pydantic.BaseModel)

    @staticmethod
    def validate_to_schema(schema: Generic[_SchemaType], data: praw) -> _SchemaType | None:

        if not isinstance(data, dict):
            dict_data = data.__dict__
        else:
            dict_data = data

        try:
            return schema.model_validate(dict_data)
        except pydantic.ValidationError:
            return None

    @staticmethod
    def validate_list_to_schema(
            data: Iterator[praw.reddit],  schema: Generic[_SchemaType]) -> list[_SchemaType]:

        result_list: list = []
        for one_data in data:
            result_list.append(ConvertSchemasMixin.validate_to_schema(schema, one_data))

        return result_list

    def get_comments_from_post(
            self,
            post: praw.reddit.Subreddit,
            limit: int = 15) -> list[RedditCommentSchema] | None:

        top_comments: list[praw.reddit.Comment] = post.comments.list()[:limit]
        result: list[RedditCommentSchema] = self.validate_list_to_schema(
            top_comments,
            RedditCommentSchema
        )

        return result

    def convert_posts_to_schema(
            self,
            all_posts: Iterator[praw.reddit.Subreddit]) -> list[RedditPostSchema]:

        result_list: list = []

        for post in all_posts:
            comments = self.get_comments_from_post(post)
            data = post.__dict__
            data['comments'] = comments
            result_list.append(self.validate_to_schema(RedditPostSchema, data))

        return result_list


class UtilsMixins:
    @staticmethod
    def count_author_posts(posts: list[RedditPostSchema]) -> list[tuple[str, int]]:
        result_dict: dict = {}
        for post in posts:
            if post.author:
                result_dict[post.author] = result_dict.get(post.author, 0) + 1

        return sorted(result_dict.items(), key=lambda x: x[1], reverse=True)

    @staticmethod
    def count_comments_by_user(posts: list[RedditPostSchema]) -> list[tuple[str, int]]:
        result_dict: dict = {}
        for post in posts:
            comments = post.comments
            if comments:
                for comment in comments:
                    if comment.author is not None:
                        result_dict[comment.author] = result_dict.get(comment.author, 0) + 1

        return sorted(result_dict.items(), key=lambda x: x[1], reverse=True)

    @staticmethod
    def presentation_poplar_comments_and_posts(
            text_type: PopularTextTypes,
            list_with_users: list[tuple[str, int]],
            limit: int = 10) -> dict[str, str]:

        result_dict: dict = {}

        for index, tuple_user_data in enumerate(list_with_users, 1):
            if index > limit:
                break
            user, count = tuple_user_data
            result_dict[f'Номер {index}'] = f'{user} - {text_type.value}: {count}шт.'

        return result_dict

    @staticmethod
    def filter_posts_by_date_range(
            posts: list[RedditPostSchema],
            day_start: datetime.datetime = datetime.datetime.utcnow(),
            days_behind: int = 3) -> list[RedditPostSchema] | None:

        datetime_behind: datetime.datetime = (day_start - datetime.timedelta(days=days_behind)
                                              ).replace(tzinfo=pytz.UTC)
        filtered_posts: Iterator = filter(
            lambda post: post is not None and post.created_at_utc >= datetime_behind, posts
        )
        filter_posts: list = list(filtered_posts)

        return filter_posts if filter_posts else None
