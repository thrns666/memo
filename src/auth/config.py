from fastapi.security import OAuth2PasswordBearer
from fastapi_users.authentication import JWTStrategy, CookieTransport, AuthenticationBackend

SECRET_KEY = 'hzcho'  # move to .env > config

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')

cookie_transport = CookieTransport(cookie_name='memo-token-cookie', cookie_max_age=6000)


def get_jwt_strategy():
    return JWTStrategy(secret=SECRET_KEY, lifetime_seconds=6000)


auth_backend = AuthenticationBackend(
    name='jwt',
    transport=cookie_transport,
    get_strategy=get_jwt_strategy
)
