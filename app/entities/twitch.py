from pydantic import BaseModel


class TwitchTokenResponse(BaseModel):
    access_token: str
    expires_in: int
    refresh_token: str
    scope: list[str]
    token_type: str


class TwitchUser(BaseModel):
    id: str
    login: str
    display_name: str
    email: str
    created_at: str
