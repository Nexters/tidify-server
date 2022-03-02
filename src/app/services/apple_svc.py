import jwt

headers = {
    'kid': 'D2KMYK4ZR5'
}

payload = {
    'iss': '787Q6972XA',
    # 'iat': timezone.now(),
    # 'exp': timezone.now() + timedelta(days=180),
    'aud': 'https://appleid.apple.com',
    'sub': 'com.nexters.tidify',
}

client_secret = jwt.encode(
    payload,
    settings.SOCIAL_AUTH_APPLE_PRIVATE_KEY,
    algorithm='ES256',
    headers=headers
).decode("utf-8")
