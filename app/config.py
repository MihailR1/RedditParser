from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    REDDIT_CLIENT_SECRET_KEY: str
    REDDIT_CLIENT_ID: str
    REDDIT_APP_NAME: str
    REDDIT_REDIRECT_URI: str
    REDDIT_USER_AGENT: str = "testscript by echobot392"
    REDDIT_BASE_URL: str = "https://www.reddit.com/"

    model_config = SettingsConfigDict(env_file='.env', extra='ignore')


settings = Settings()
