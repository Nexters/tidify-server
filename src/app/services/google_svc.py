from urllib.parse import urlencode

from pydantic.dataclasses import dataclass


@dataclass
class GoogleOAuthToken:
    access_token: str
    expires_in: int
    id_token: str
    scope: str
    token_type: str
    # refresh_token: Optional[str]


# https://developers.google.com/identity/protocols/oauth2/openid-connect#authenticationuriparameters
def get_google_auth_url(settings, callback_uri, state):
    # nonce = uuid.uuid4()
    query = {
        'response_type': 'code',
        'client_id': settings.GOOGLE_CLIENT_ID,
        'scope': 'openid email',
        'redirect_uri': callback_uri,
        # 'nonce': nonce,       # id_token 안에 nonce 랑 비교해야 함.
        'state': state
    }
    return f'{settings.GOOGLE_AUTH_URL}?{urlencode(query)}'

async def get_auth_code(settings, google_auth_code, redirect_uri):
    user_email = await get_user_email(settings, google_auth_code, redirect_uri)
    return await generate_auth_code(user_email, User.OAuthService.GOOGLE)


async def get_user_email(settings, auth_code, redirect_uri):
    oauth: GoogleOAuthToken = await get_access_token(settings.GOOGLE_TOKEN_URL,
                                                     settings.GOOGLE_CLIENT_ID,
                                                     settings.GOOGLE_CLIENT_SECRET,
                                                     settings.PROXY,
                                                     redirect_uri,
                                                     auth_code)
    logging.debug(oauth)
    id_token_payload = parse_id_token(settings.GOOGLE_CLIENT_ID, oauth.id_token)

    if is_valid_id_token(id_token_payload, settings.GOOGLE_CLIENT_ID):
        return id_token_payload['email']
    else:
        raise InternalServerError()


async def get_access_token(token_url, client_id, client_secret, proxy, redirect_uri, code):
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    params = {
        'code': code,
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'authorization_code',
        'redirect_uri': str(redirect_uri)
    }

    async with requests_timeout() as session:
        logging.debug(session)
        try:
            async with session.post(url=token_url, headers=headers, params=params, proxy=proxy) as response:
                logging.debug(response)
                if response.status != status.HTTP_200_OK:
                    raise GoogleOAuthError()
                result = await response.json()
                return GoogleOAuthToken(**result)

        except Exception as e:
            raise GoogleOAuthError()

