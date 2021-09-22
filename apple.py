# -*- coding: utf-8 -*-


import hashlib
import json
import os

from authlib.integrations.base_client import OAuthError
from authlib.integrations.starlette_client import OAuth
from fastapi import FastAPI
from pydantic import typing
from starlette.config import Config
from starlette.middleware.sessions import SessionMiddleware
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse

_SECRET_KEY = hashlib.sha256(os.urandom(1024)).hexdigest()

oauth_client = FastAPI()
oauth_client.add_middleware(SessionMiddleware, secret_key=_SECRET_KEY)

# os.getenv
config = Config('.env')
oauth = OAuth(config)
oauth.register(
    name='apple',
    server_metadata_url='https://appleid.apple.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email name'
    }
)  # apple은 profile image 없다.

"""
auth:
  apple:
    token-url: https://appleid.apple.com/auth/token
    public-keys-url: https://appleid.apple.com/auth/keys
    iss: https://appleid.apple.com
    aud: com.nexters.tidify
    team-id: 787Q6972XA
    private-key:
      id: D2KMYK4ZR5
      path: AuthKey_D2KMYK4ZR5.p8
"""

import pprint

pp = pprint.PrettyPrinter(indent=4)


def _pretty(d):
    pp.pprint(d)


def _beautify_print(idx, help_text, raw_data: typing.Dict):
    print(f'{idx}.{help_text} start #######################################')
    _pretty(raw_data)
    print(f'{idx}.{help_text} finished #######################################')


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
    _beautify_print(1, "request for login", request.__dict__)
    redirect_uri = request.url_for('sign_in')
    return await oauth.apple.authorize_redirect(request=request, redirect_uri=redirect_uri)


@oauth_client.route('/sign_in')
async def sign_in(request: Request):
    _beautify_print(2, "redirect for sign_in", request.__dict__)
    try:
        token = await oauth.apple.authorize_access_token(request)
        _beautify_print(3, "redirect with token", token)
    except OAuthError as error:
        return HTMLResponse(f'<h1>{error.error}</h1>')

    user = await oauth.apple.parse_id_token(request, token)
    _beautify_print(4, "user info", dict(user))
    request.session['user'] = dict(user)
    return RedirectResponse(url='/')


@oauth_client.get('/logout')
async def logout(request: Request):
    request.session.pop('user', None)
    return RedirectResponse(url='/')


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(oauth_client, host='127.0.0.1', port=8080)



