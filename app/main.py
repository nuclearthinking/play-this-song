import logging

from fastapi import Depends, FastAPI
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette.staticfiles import StaticFiles

from app.dependencies import auth_as_user
from app.exceptions import NotAuthorizedException
from app.routers import editor, login
from app.schemes.twitch import TwitchUser

logger = logging.getLogger()


app = FastAPI()

app.include_router(login.router)
app.include_router(editor.router)

app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.exception_handler(NotAuthorizedException)
async def not_authorized_redirect(*_, **__) -> RedirectResponse:
    return RedirectResponse(url="/login")


@app.get("/", response_class=HTMLResponse)
async def root(_: TwitchUser = Depends(auth_as_user)):
    with open("app/static/index.html", "r", encoding="utf8") as index_html:
        html_response = index_html.read()
    return HTMLResponse(
        content=html_response,
        status_code=200,
        media_type="text/html",
    )
