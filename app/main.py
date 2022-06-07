import logging

from fastapi import Depends, FastAPI
from starlette.responses import RedirectResponse

from app.dependencies import cookie_auth
from app.entities.twitch import TwitchUser
from app.exceptions import NotAuthorizedException
from app.routers import login

app = FastAPI()
app.include_router(login.router)

logger = logging.getLogger()


@app.exception_handler(NotAuthorizedException)
async def not_authorized_redirect(
    *_,
    **__,
) -> RedirectResponse:
    return RedirectResponse(url="/login")


@app.get("/")
async def root(auth_user: TwitchUser = Depends(cookie_auth)):
    return auth_user.dict()
