from datetime import timedelta

from fastapi import APIRouter, Request
from jose import jwt
from starlette.responses import RedirectResponse

from app.config import settings
from app.schemes.twitch import TwitchUser
from app.services.twitch_api.auth import get_access_token, get_twitch_auth_url, get_user_data

router = APIRouter()


def user_to_cookie(user: TwitchUser) -> str:
    data = user.dict().copy()
    return jwt.encode(data, settings.jwt_secret)


@router.get("/auth/callback")
async def oauth_callback(request: Request) -> RedirectResponse:
    code = request.query_params.get("code")
    access_token = await get_access_token(code=code)
    user_data = await get_user_data(access_token)
    response = RedirectResponse(
        url="/",
    )
    response.set_cookie(
        key="SL_AUTH",
        value=user_to_cookie(user_data),
        expires=int(timedelta(days=7).total_seconds()),
    )
    return response


@router.get("/login")
async def login():
    response = RedirectResponse(url=get_twitch_auth_url())
    return response
