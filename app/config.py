import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    REDDIT_CLIENT_SECRET_KEY: str
    REDDIT_CLIENT_ID: str
    REDDIT_APP_NAME: str
    REDDIT_REDIRECT_URI: str
    REDDIT_USER_AGENT: str = "testscript by echobot392"
    REDDIT_BASE_URL: str = "https://www.reddit.com/"

    BASEDIR: str = os.path.abspath(os.path.dirname(__file__))
    ENV_FILE_PATH: str = os.path.join(BASEDIR, '..', '.env')

    model_config = SettingsConfigDict(env_file=ENV_FILE_PATH, extra='ignore')


settings = Settings()
