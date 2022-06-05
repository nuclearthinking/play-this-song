from fastapi import Request
from fastapi.security.base import SecurityBase
from jose import jwt
from jose.constants import ALGORITHMS

from app.config import JWT_SECRET
from app.entities.twitch import TwitchUser
from app.exceptions import NotAuthorizedException


class CookieAuth(SecurityBase):
    def __init__(self, scheme_name: str = None, auto_error: bool = True):
        self.scheme_name = scheme_name or self.__class__.__name__
        self.auto_error = auto_error

    async def __call__(self, request: Request) -> TwitchUser:
        authorization: str = request.cookies.get("SL_AUTH")
        if not authorization:
            raise NotAuthorizedException("User is not authorized")
        if authorization:
            return cookie_to_user(authorization)


def cookie_to_user(cookie: str) -> TwitchUser:
    return TwitchUser.parse_obj(
        jwt.decode(token=cookie, key=JWT_SECRET, algorithms=[ALGORITHMS.HS256])
    )


cookie_auth = CookieAuth()
