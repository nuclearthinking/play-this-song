from fastapi import Request
from fastapi.security.base import SecurityBase
from jose import jwt
from jose.constants import ALGORITHMS

from app.config import settings
from app.exceptions import NotAuthorizedException, NotEnoughPermissions
from app.schemes.twitch import TwitchUser


class CookieAuth(SecurityBase):
    def __init__(self, scheme_name: str = None, admin_users=None):
        if admin_users is None:
            admin_users = []
        self.scheme_name = scheme_name or self.__class__.__name__
        self.admin_users = admin_users

    async def __call__(self, request: Request) -> TwitchUser:
        authorization: str = request.cookies.get("SL_AUTH")
        if not authorization:
            raise NotAuthorizedException("User is not authorized")
        user = cookie_to_user(authorization)
        if self.admin_users and user.login not in self.admin_users:
            raise NotEnoughPermissions("You have no access to this area")
        return user


def cookie_to_user(cookie: str) -> TwitchUser:
    return TwitchUser.parse_obj(jwt.decode(token=cookie, key=settings.jwt_secret, algorithms=[ALGORITHMS.HS256]))


auth_as_user = CookieAuth()

auth_as_admin = CookieAuth(admin_users=["nuclearthinking"])
