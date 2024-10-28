from fastapi.security import OAuth2PasswordBearer

SECRET_KEY = 'hzcho'
ALGORITHM = 'HS256'

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')
