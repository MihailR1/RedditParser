from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    REDDIT_CLIENT_SECRET_KEY: str
    REDDIT_CLIENT_ID: str
    REDDIT_APP_NAME: str
    REDDIT_REDIRECT_URI: str
    REDDIT_USER_AGENT: str = 'testscript by echobot392'
    REDDIT_BASE_URL: str = 'https://www.reddit.com/'

    class Config:
        env_file = "../.env"


settings = Settings()
