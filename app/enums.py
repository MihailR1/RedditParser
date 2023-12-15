import enum


class PopularTextTypes(enum.Enum):
    comment = "комментариев"
    post = "постов"


class TimeFilterPosts(enum.Enum):
    all = 'all'
    week = 'week'
    month = 'month'
    year = 'year'
