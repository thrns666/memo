import jwt
from fastapi import Depends

from src.auth.config import SECRET_KEY, ALGORITHM, oauth2_scheme


def create_jwt_token(data: dict):
    return jwt.encode(payload=data, key=SECRET_KEY, algorithm=ALGORITHM)


def get_user_from_token(token: str = Depends(oauth2_scheme)):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return payload.get('sub')
