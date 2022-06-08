import aiohttp

from app.config import REDIRECT_URI, TWITCH_CLIENT_ID, TWITCH_SECRET, TWITCH_TOKEN_URI
from app.entities.twitch import TwitchTokenResponse, TwitchUser


async def get_access_token(code: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.post(
            url=TWITCH_TOKEN_URI,
            data={
                "client_id": TWITCH_CLIENT_ID,
                "client_secret": TWITCH_SECRET,
                "code": code,
                "redirect_uri": REDIRECT_URI,
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
                "Client-Id": TWITCH_CLIENT_ID,
            },
        ) as response:
            response_body = await response.json()
            return TwitchUser.parse_obj(response_body["data"][0])
