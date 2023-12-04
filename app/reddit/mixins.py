import datetime
from typing import Iterator

import praw

from app.config import settings
from app.enums import PopularTextTypes
from app.schemas import RedditPostSchema, SubbReditSchema


class ConvertSchemasMixin:
    @staticmethod
    def convert_subreddits_to_schema(
            subbredits: list[praw.reddit.Subreddit]) -> list[SubbReditSchema]:

        subbredits_list: list = []

        for index, subreddit in enumerate(subbredits, 1):
            full_url = settings.REDDIT_BASE_URL + subreddit.url
            *_, name_subbredit, _ = subreddit.url.split('/')
            subbredits_list.append(
                SubbReditSchema.model_validate(
                    {'index': index, 'name': name_subbredit, 'full_url': full_url}
                ))

        return subbredits_list

    @staticmethod
    def convert_comment_to_schema(comment: praw.reddit.Comment) -> dict[str, str | int] | None:
        result_dict = {}
        try:
            author = comment.author.name
            author_id = comment.author_fullname
            datetime_post = datetime.datetime.fromtimestamp(comment.created_utc)
            score = comment.score
            comment_txt = comment.body
            link = settings.REDDIT_BASE_URL + comment.permalink

            result_dict = {
                'author': author,
                'author_id': author_id,
                'datetime_post': datetime_post,
                'score': score,
                'comment_text': comment_txt,
                'link': link
            }
        except AttributeError:
            "Если автор комментария удалил свой аккаунт, то получить имя автора не получится - будет ошибка"
            pass

        return result_dict if result_dict else None

    def convert_posts_to_schema(
            self, subbredit_name: str,
            all_posts: Iterator[praw.reddit.Subreddit]) -> list[RedditPostSchema]:

        result_list: list = []

        for post in all_posts:
            try:
                title = post.title
                author = post.author.name
                author_id = post.author_fullname
                subbreddit_name = subbredit_name
                created_at_utc = datetime.datetime.fromtimestamp(post.created_utc)
                full_url = settings.REDDIT_BASE_URL + post.permalink
                number_of_comments = post.num_comments
                score = post.score
                ups = post.ups
                comments = self.get_comments_from_post(post)
                result_dict = {
                    'title': title,
                    'author': author,
                    'author_id': author_id,
                    'subbreddit_name': subbreddit_name,
                    'created_at_utc': created_at_utc,
                    'full_url': full_url,
                    'number_of_comments': number_of_comments,
                    'score': score,
                    'ups': ups,
                    'comments': comments
                }
                result_list.append(RedditPostSchema.model_validate(result_dict))
            except AttributeError:
                "Если автор поста удалил свой аккаунт, то получить имя автора не получится - будет ошибка"
                continue

        return result_list


class CountMixins:
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
            limit: int = 10) -> dict[str | str]:

        result_dict: dict = {}

        for index, tuple_user_data in enumerate(list_with_users, 1):
            if index > limit:
                break
            user, count = tuple_user_data
            result_dict[f'Номер {index}'] = f'{user} - {text_type.value}: {count}шт.'

        return result_dict


class FilterPostMixin:
    @staticmethod
    def get_datetime_few_days_behind(
            date_start: datetime.datetime = datetime.datetime.utcnow(),
            days_behind: int = 3) -> datetime.datetime:

        new_date = date_start - datetime.timedelta(days=days_behind)

        return new_date

    def filter_posts_by_date_range(
            self,
            posts: list[RedditPostSchema],
            day_start: datetime.datetime = datetime.datetime.utcnow(),
            days_behind: int = 3) -> list[RedditPostSchema]:

        datetime_behind: datetime.datetime = self.get_datetime_few_days_behind(day_start, days_behind)
        filtered_posts = [post for post in posts if post.created_at_utc >= datetime_behind]
        return filtered_posts
