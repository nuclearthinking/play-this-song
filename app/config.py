import os

TWITCH_AUTH_URI = "https://id.twitch.tv/oauth2/authorize"
TWITCH_TOKEN_URI = "https://id.twitch.tv/oauth2/token"
TWITCH_SECRET = os.getenv("SECRET_KEY")
TWITCH_CLIENT_ID = os.getenv("CLIENT_ID")
TWITCH_SCOPES = "user:read:email user:read:follows"

REDIRECT_URI = "http://localhost:8000/auth/callback"

JWT_SECRET = os.getenv("JWT_SECRET")
