import datetime
from typing import Iterator

import praw

from config import settings
from schema import SubbReditSchema, RedditPostSchema, RedditCommentSchema

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


def get_comments_from_post(post: praw.models.reddit.submission.Submission, limit: int = 200) -> list[RedditCommentSchema] | None:
    top_comments = post.comments.list()[:limit]
    result_list = []
    for comment in top_comments:
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
            result_list.append(RedditCommentSchema.model_validate(result_dict))
        except AttributeError:
            "Если автор комментария удалил свой аккаунт, то получить имя автора не получится - будет ошибка"
            continue

    return result_list if result_list else None


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
        comments = get_comments_from_post(post)
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

    return result_list


def grab_hot_posts_from_subbredid(subbredid: SubbReditSchema, limit=200) -> list[RedditPostSchema]:
    top_posts = reddit.subreddit(subbredid.name).hot(limit=limit)
    post_parsed_as_schema = convert_posts_to_schema(subbredid.name, top_posts)
    return post_parsed_as_schema


def get_datetime_few_days_behind(date_start: datetime.datetime = datetime.datetime.utcnow(),
                                 days_behind: int = 3) -> datetime.datetime:
    new_date = date_start - datetime.timedelta(days=days_behind)
    return new_date


def filter_posts_by_date_range(posts: list[RedditPostSchema],
                               day_start: datetime.datetime = datetime.datetime.utcnow(),
                               days_behind: datetime.datetime = 3) -> list[RedditPostSchema]:
    datetime_behind = get_datetime_few_days_behind(day_start, days_behind)
    filtered_posts = [post for post in posts if post.created_at_utc >= datetime_behind]
    return filtered_posts


def count_author_posts(posts: list[RedditPostSchema]) -> list[tuple[str, int]]:
    result_dict = {}
    for post in posts:
        result_dict[post.author] = result_dict.get(post.author, 0) + 1

    return sorted(result_dict.items(), key=lambda x: x[1], reverse=True)


def count_comments_by_user(posts: list[RedditPostSchema]) -> list[tuple[str, int]]:
    result_dict = {}
    for post in posts:
        comments = post.comments
        if comments:
            for comment in comments:
                result_dict[comment.author] = result_dict.get(comment.author, 0) + 1

    return sorted(result_dict.items(), key=lambda x: x[1], reverse=True)


ree23 = SubbReditSchema.model_validate({'index': 1, 'name': 'todayilearned', 'full_url': 'https://www.reddit.com/r/wholesomememes/comments/189qrri/old_but_gold_template/'})
res = grab_hot_posts_from_subbredid(ree23, limit=50)
filter = filter_posts_by_date_range(res)
print(count_author_posts(filter))
print(count_comments_by_user(filter))
