from app.Enums import PopularTextTypes
from app.redit_app import Reddit

if __name__ == "__main__":
    reddit = Reddit()
    popular_subreditd = reddit.get_list_of_popular_subreddits()
    user_choise_subbreddit = reddit.ask_user_for_subbredit_id_to_parse(popular_subreditd)
    grab_posts = reddit.grab_hot_posts_from_subbredid(user_choise_subbreddit, limit=50)
    filtered_posts = reddit.filter_posts_by_date_range(grab_posts)
    count_users_posts = reddit.count_author_posts(filtered_posts)
    count_users_comments = reddit.count_comments_by_user(filtered_posts)
    reddit.print_most_popular(PopularTextTypes.comment, count_users_comments)
    reddit.print_most_popular(PopularTextTypes.post, count_users_posts)
