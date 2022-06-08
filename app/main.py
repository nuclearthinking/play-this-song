import logging

from fastapi import Depends, FastAPI
from starlette.responses import RedirectResponse

from app.dependencies import auth_as_user
from app.entities.twitch import TwitchUser
from app.exceptions import NotAuthorizedException
from app.routers import editor, login

app = FastAPI()

app.include_router(login.router)
app.include_router(editor.router)


logger = logging.getLogger()


@app.exception_handler(NotAuthorizedException)
async def not_authorized_redirect(
    *_,
    **__,
) -> RedirectResponse:
    return RedirectResponse(url="/login")


@app.get("/")
async def root(auth_user: TwitchUser = Depends(auth_as_user)):
    return auth_user.dict()
