import dataclasses
from typing import Iterator, Callable

import praw

from app.schema import SubbReditSchema
from config import settings


@dataclasses.dataclass(slots=True)
class Reddit:
    reddit: praw.Reddit = praw.Reddit(
        client_id=settings.REDDIT_CLIENT_ID,
        client_secret=settings.REDDIT_CLIENT_SECRET_KEY,
        redirect_uri=settings.REDDIT_REDIRECT_URI,
        user_agent=settings.REDDIT_USER_AGENT,
    )
    subbredits_list: list[SubbReditSchema] = None

    def __post_init__(self):
        self.subbredits_list = self.get_list_of_popular_subreddits()

    def get_list_of_popular_subreddits(self) -> list[SubbReditSchema]:
        reddits_iterator = self.reddit.subreddits.popular()
        subbredits_parsed_to_schema = self.parse_subreddits_to_schema(reddits_iterator)
        return subbredits_parsed_to_schema

    @staticmethod
    def parse_subreddits_to_schema(subbredits: Iterator) -> list[SubbReditSchema]:
        subbredits_list = []
        for index, subreddit in enumerate(subbredits, 1):
            full_url = settings.REDDIT_BASE_URL + subreddit.url
            *_, name_subbredit, _ = subreddit.url.split('/')
            subbredits_list.append(
                SubbReditSchema.model_validate({'index': index, 'name': name_subbredit, 'full_url': full_url}))
        return subbredits_list

