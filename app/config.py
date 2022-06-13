import os
from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    twitch_auth_uri = "https://id.twitch.tv/oauth2/authorize"
    twitch_token_uri = "https://id.twitch.tv/oauth2/token"
    twitch_secret = os.getenv("SECRET_KEY")
    twitch_client_id = os.getenv("CLIENT_ID")
    twitch_scope = "user:read:email user:read:follows"
    redirect_uri = "http://localhost:8000/auth/callback"

    jwt_secret = os.getenv("JWT_SECRET")

    database_uri = "mysql+aiomysql://play_this_song:pass@localhost/play_this_song"


@lru_cache
def get_settings() -> Settings:

    return Settings()


settings = get_settings()
