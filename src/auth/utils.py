import jwt
from starlette.requests import Request

from src.auth.config import SECRET_KEY, ALGORITHM


def create_jwt_token(data: dict):
    return jwt.encode(payload=data, key=SECRET_KEY, algorithm=ALGORITHM)


def get_user_from_token(request: Request):
    token = request.cookies.get('auth_token')
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return payload.get('sub')
