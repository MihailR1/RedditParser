import datetime
from typing import Iterator

import praw

from app.config import settings
from app.enums import PopularTextTypes
from app.schemas import RedditPostSchema, SubredditSchema, RedditCommentSchema


class ConvertSchemasMixin:
    @staticmethod
    def convert_subreddits_to_schema(
            subreddits: Iterator[praw.reddit.Subreddit]) -> list[SubredditSchema]:

        subreddits_list: list = []

        for index, subreddit in enumerate(subreddits, 1):
            full_url = settings.REDDIT_BASE_URL + subreddit.url
            *_, name_subreddit, _ = subreddit.url.split('/')
            subreddits_list.append(
                SubredditSchema.model_validate(
                    {'index': index, 'name': name_subreddit, 'full_url': full_url}
                ))

        return subreddits_list

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

    def get_comments_from_post(
            self,
            post: praw.reddit.Subreddit,
            limit: int = 15) -> list[RedditCommentSchema] | None:

        top_comments: list[praw.reddit.Comment] = post.comments.list()[:limit]
        result_list: list = []

        for comment in top_comments:
            parsed_comment: dict[str, str | int] | None = self.convert_comment_to_schema(comment)
            if parsed_comment:
                result_list.append(parsed_comment)

        return result_list if result_list else None

    def convert_posts_to_schema(
            self, subreddit_name: str,
            all_posts: Iterator[praw.reddit.Subreddit]) -> list[RedditPostSchema]:

        result_list: list = []

        for post in all_posts:
            try:
                title = post.title
                author = post.author.name
                author_id = post.author_fullname
                subreddit_name = subreddit_name
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
                    'subreddit_name': subreddit_name,
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
            limit: int = 10) -> dict[str, str]:

        result_dict: dict = {}

        for index, tuple_user_data in enumerate(list_with_users, 1):
            if index > limit:
                break
            user, count = tuple_user_data
            result_dict[f'Номер {index}'] = f'{user} - {text_type.value}: {count}шт.'

        return result_dict
