# -*- coding: utf-8 -*-
"""
https://github.com/authlib/demo-oauth-client/blob/master/fastapi-google-login/app.py
"""

import hashlib
import json
import os

from authlib.integrations.base_client import OAuthError
from authlib.integrations.starlette_client import OAuth
from fastapi import FastAPI
from starlette.config import Config
from starlette.middleware.sessions import SessionMiddleware
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse

_SECRET_KEY = hashlib.sha256(os.urandom(1024)).hexdigest()
_CLIENT_SECRETS_FILE = "client_secret.json"

oauth_client = FastAPI()
oauth_client.add_middleware(SessionMiddleware, secret_key=_SECRET_KEY)

config = Config(".google.env")
oauth = OAuth(config)
oauth.register(
        name='google',
        server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
        client_kwargs={
            'scope': 'openid email profile'
        }
)


@oauth_client.get('/')
async def homepage(request: Request):
    user = request.session.get('user')
    if user:
        data = json.dumps(user)
        html = (
            f'<pre>{data}</pre>'
            '<a href="/logout">logout</a>'
        )
        return HTMLResponse(html)
    return HTMLResponse('<a href="/login">login</a>')


@oauth_client.route('/login')
async def login(request: Request):
    redirect_uri = request.url_for('sign_in')
    tmp = await oauth.google.authorize_redirect(request=request, redirect_uri=redirect_uri)
    return tmp


@oauth_client.route('/sign_in')
async def sign_in(request: Request):
    try:
        token = await oauth.google.authorize_access_token(request)
    except OAuthError as error:
        return HTMLResponse(f'<h1>{error.error}</h1>')

    user = await oauth.google.parse_id_token(request, token)
    request.session['user'] = dict(user)
    return RedirectResponse(url='/')


@oauth_client.get('/logout')
async def logout(request: Request):
    request.session.pop('user', None)
    return RedirectResponse(url='/')


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(oauth_client, host='127.0.0.1', port=8080)
