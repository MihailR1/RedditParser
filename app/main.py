import datetime
from typing import Iterator

import praw

from config import settings
from schema import SubbReditSchema, RedditPostSchema

# Ваша задача – написать скрипт, который спрашивает сабреддит, парсит с него все посты за последние 3 дня и
# выводит топ пользователей, которые написали больше всего комментариев и топ пользователей,
# которые написали больше всего постов. Топ - это когда сверху тот, кто
# больше всех написал комментариев/постов, на втором месте следущий за ним и так далее.

reddit = praw.Reddit(
    client_id=settings.REDDIT_CLIENT_ID,
    client_secret=settings.REDDIT_CLIENT_SECRET_KEY,
    redirect_uri=settings.REDDIT_REDIRECT_URI,
    user_agent=settings.REDDIT_USER_AGENT,
)


def get_list_of_popular_subreddits() -> Iterator:
    return reddit.subreddits.popular()


def parse_subreddits_to_schema(subbredits: Iterator[praw.models.Subreddit]) -> list[SubbReditSchema]:
    subbredits_list = []
    for index, subreddit in enumerate(subbredits, 1):
        full_url = settings.REDDIT_BASE_URL + subreddit.url
        *_, name_subbredit, _ = subreddit.url.split('/')
        subbredits_list.append(
            SubbReditSchema.model_validate({'index': index, 'name': name_subbredit, 'full_url': full_url}))
    return subbredits_list


def print_subbredits_list(subbredits: list[SubbReditSchema], limit: int = 20) -> None:
    for subred in subbredits:
        if subred.index > limit:
            break
        print(f'{subred.index} - {subred.name}')


def get_subreddit_by_index(subbredits: list[SubbReditSchema], index: int) -> SubbReditSchema:
    for subred in subbredits:
        if subred.index == index:
            return subred


def ask_user_for_subbredit_id_to_parse(subbredits: list[SubbReditSchema]) -> int | None:
    user_choice = None
    succes_flag = False
    limit_to_show_subbredits = 15
    print_subbredits_list(subbredits, limit=limit_to_show_subbredits)
    while succes_flag is not True:
        try:
            user_choice = int(input('Введите номер интересующего subbredit: '))
            if user_choice > 0 and user_choice <= limit_to_show_subbredits:
                succes_flag = True
            else:
                raise ValueError
        except ValueError:
            print('Ввидет только номер существующего саббредита')
    return user_choice


def convert_posts_to_schema(subbredit_name: str, all_posts: Iterator[praw.models.Subreddit]) -> list[RedditPostSchema]:
    result_list = []

    for post in all_posts:
        title = post.title
        author = post.author.name
        author_id = post.author_fullname
        subbreddit_name = subbredit_name
        created_at_utc = datetime.datetime.fromtimestamp(post.created_utc)
        full_url = settings.REDDIT_BASE_URL + post.permalink
        number_of_comments = post.num_comments
        score = post.score
        ups = post.ups
        result_dict = {
            'title': title,
            'author': author,
            'author_id': author_id,
            'subbreddit_name': subbreddit_name,
            'created_at_utc': created_at_utc,
            'full_url': full_url,
            'number_of_comments': number_of_comments,
            'score': score,
            'ups': ups
        }
        result_list.append(RedditPostSchema.model_validate(result_dict))

    return result_list


def grab_hot_posts_from_subbredid(subbredid: SubbReditSchema, limit=200) -> list[RedditPostSchema]:
    top_posts = reddit.subreddit(subbredid.name).hot(limit=limit)
    post_parsed_as_schema = convert_posts_to_schema(subbredid.name, top_posts)
    return post_parsed_as_schema

ree23 = SubbReditSchema.model_validate({'index': 1, 'name': 'todayilearned', 'full_url': 'todayilearned'})
res = grab_hot_posts_from_subbredid(ree23, 2)
print(res)