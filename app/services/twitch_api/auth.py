import uuid
from urllib import parse

import aiohttp

from app.config import settings
from app.schemes.twitch import TwitchTokenResponse, TwitchUser


async def get_access_token(code: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.post(
            url=settings.twitch_token_uri,
            data={
                "client_id": settings.twitch_client_id,
                "client_secret": settings.twitch_secret,
                "code": code,
                "redirect_uri": settings.redirect_uri,
                "grant_type": "authorization_code",
            },
        ) as response:
            response_body = await response.json()
            token_response = TwitchTokenResponse.parse_obj(response_body)
            return token_response.access_token


async def get_user_data(access_token: str) -> TwitchUser:
    async with aiohttp.ClientSession() as session:
        async with session.get(
            url="https://api.twitch.tv/helix/users",
            headers={
                "Authorization": f"Bearer {access_token}",
                "Client-Id": settings.twitch_client_id,
            },
        ) as response:
            response_body = await response.json()
            return TwitchUser.parse_obj(response_body["data"][0])


def get_twitch_auth_url() -> str:
    return f"{settings.twitch_auth_uri}?" + parse.urlencode(
        {
            "response_type": "code",
            "client_id": settings.twitch_client_id,
            "redirect_uri": settings.redirect_uri,
            "scope": settings.twitch_scope,
            "state": str(uuid.uuid4()),
        }
    )
