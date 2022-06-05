import logging
import uuid
from urllib import parse

import aiohttp
import os
from fastapi import Depends, FastAPI, Request
from fastapi.security.base import SecurityBase
from jose import jwt
from jose.constants import ALGORITHMS
from pydantic import BaseModel
from starlette.responses import RedirectResponse

app = FastAPI()

twitch_auth_uri = "https://id.twitch.tv/oauth2/authorize"
twitch_token_uri = "https://id.twitch.tv/oauth2/token"
secret_key = os.getenv('SECRET_KEY')
app_id = os.getenv('CLIENT_ID')
jwt_secret = os.getenv('JWT_SECRET')
scopes = "user:read:email user:read:follows"
redirect_uri = "http://localhost:8000/auth/callback"

logger = logging.getLogger()


class SongListBaseException(Exception):
    pass


class NotAuthorizedException(SongListBaseException):
    ...


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


class CookieAuth(SecurityBase):
    def __init__(self, scheme_name: str = None, auto_error: bool = True):
        self.scheme_name = scheme_name or self.__class__.__name__
        self.auto_error = auto_error

    async def __call__(self, request: Request) -> TwitchUser | RedirectResponse:
        authorization: str = request.cookies.get("SL_AUTH")
        if not authorization:
            raise NotAuthorizedException("User is not authorized")
        if authorization:
            return cookie_to_user(authorization)


cookie_auth = CookieAuth()


def user_to_cookie(user: TwitchUser) -> str:
    data = user.dict().copy()
    return jwt.encode(data, jwt_secret)


def cookie_to_user(cookie: str) -> TwitchUser:
    return TwitchUser.parse_obj(
        jwt.decode(token=cookie, key=jwt_secret, algorithms=[ALGORITHMS.HS256])
    )


@app.exception_handler(NotAuthorizedException)
async def not_authorized_redirect(
    request: Request, exception: NotAuthorizedException
) -> RedirectResponse:
    return RedirectResponse(url="/login")


@app.get("/")
async def root(auth_user: TwitchUser = Depends(cookie_auth)):
    return auth_user.dict()


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.get("/auth/callback")
async def oauth_callback(request: Request) -> RedirectResponse:
    code = request.query_params.get("code")
    access_token = await get_access_token(code=code)
    user_data = await get_user_data(access_token)
    response = RedirectResponse(
        url="/",
    )
    response.set_cookie(key="SL_AUTH", value=user_to_cookie(user_data))
    return response


@app.get("/login")
async def login():
    auth_url = f"{twitch_auth_uri}?" + parse.urlencode(
        {
            "response_type": "code",
            "client_id": app_id,
            "redirect_uri": redirect_uri,
            "scope": scopes,
            "state": str(uuid.uuid4()),
        }
    )
    response = RedirectResponse(url=auth_url)
    return response


async def get_access_token(code: str) -> str:

    async with aiohttp.ClientSession() as session:
        async with session.post(
            url=twitch_token_uri,
            data={
                "client_id": app_id,
                "client_secret": secret_key,
                "code": code,
                "redirect_uri": redirect_uri,
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
                "Client-Id": app_id,
            },
        ) as response:
            response_body = await response.json()
            return TwitchUser.parse_obj(response_body["data"][0])
