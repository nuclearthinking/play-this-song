import uuid
from datetime import timedelta
from urllib import parse

from fastapi import APIRouter, Request
from jose import jwt
from starlette.responses import RedirectResponse

from app.config import (JWT_SECRET, REDIRECT_URI, TWITCH_AUTH_URI,
                        TWITCH_CLIENT_ID, TWITCH_SCOPES)
from app.entities.twitch import TwitchUser
from app.services.twitch_api.auth import get_access_token, get_user_data

router = APIRouter()


def user_to_cookie(user: TwitchUser) -> str:
    data = user.dict().copy()
    return jwt.encode(data, JWT_SECRET)


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
    auth_url = f"{TWITCH_AUTH_URI}?" + parse.urlencode(
        {
            "response_type": "code",
            "client_id": TWITCH_CLIENT_ID,
            "redirect_uri": REDIRECT_URI,
            "scope": TWITCH_SCOPES,
            "state": str(uuid.uuid4()),
        }
    )
    response = RedirectResponse(url=auth_url)
    return response
