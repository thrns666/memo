from fastapi import APIRouter, HTTPException, Depends
from loguru import logger
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.templating import Jinja2Templates

from celery_config.celery_tasks import send_mail_with_pass
from postgre_db import crud
from postgre_db.crud import get_session
from postgre_db.dao import UserDAO
from postgre_db.schemas import LoginUser, RegisterUser
from redis_config.redis_crud import get_from_redis

auth_router = APIRouter()
templates = Jinja2Templates(directory='static/templates')

# user: Пароль для входа на почту smtp -> jwt token expire == 60*1440(24h) header/cookie
# guest: create jwt token(expire == 60*20) -> anonym note expire(24h) stash from postgres


@auth_router.get('/login')
async def login_user(request: Request):
    return templates.TemplateResponse(request=request, name='login_page_0.html', status_code=200)


@auth_router.post('/login')
async def login(request: Request, data: LoginUser):
    try:
        user = UserDAO.get_one_or_none(email=data.email)
        if user:
            await send_mail_with_pass(data.email)
        context = {'test': 'context'}                           # mb in headers put email login??????
        return templates.TemplateResponse(request=request, name='login_form_1.html', context=context, status_code=200)
    except Exception as ex:
        logger.error(f'Error in login user: {ex}')
        return HTTPException(status_code=500, detail=ex)


@auth_router.post('/password')
async def check_password(email: EmailStr, password: str):
    res = get_from_redis(email)
    if res and res == password:
        jwt_token = 'create_jwt_token(expire=24h)'
        return 'Response(headers=jwt_token)'


@auth_router.post('/create_user')
async def create_user(data: RegisterUser, session: AsyncSession = Depends(get_session)):
    try:
        await crud.create_user(session=session, name=data.name, email=data.email)
        logger.info(f'Created new user: {data.name} - {data.email}')
        # celery_config task sends mail???
    except Exception as ex:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'err': ex})

    return JSONResponse(status_code=status.HTTP_201_CREATED, content={'data': [_ for _ in data]})

###############
# def create_jwt_token(data: dict):
#     return jwt.encode(payload=data, key=SECRET_KEY, algorithm=ALGORITHM)
#
#
# def get_user_from_token(token: str = Depends(oauth2_scheme)):
#         try:
#             payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#             return payload.get('sub')
#         except jwt.ExpiredSignatureError:
#             raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token has expire', headers={
#                 'WWW-Authenticate': 'Bearer'
#             })
#         except jwt.InvalidTokenError:
#             raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid token', headers={
#                 'WWW-Authenticate': 'Bearer'
#             })
#
#
# def decode_password(hashed_password: str):
#     if hashed_password[:-15]:
#         return hashed_password[:-15]
#
#
# @auth.post('/token')
# async def login(user_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
#     user_data_from_db: models.User = crud.get_user(db=db, email=user_data.username)
#     if user_data_from_db is None or user_data.password != decode_password(user_data_from_db.hashed_password):
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid credentials', headers={
#             'WWW-Authenticate': 'Bearer'
#         })
#     return {'access_toke': create_jwt_token(
#         {
#             'sub': {
#                 'username': user_data_from_db.email,
#                 'role': user_data_from_db.role
#             },
#             'exp': datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(seconds=300)
#         }
#     ),
#         'token_type': 'bearer'}
#
#
# @auth.get('/token')
# async def guest_token() -> dict:
#     return {'guest_token': create_jwt_token({'sub': {'role': 'guest'}, 'exp': datetime.datetime.now(
#         tz=datetime.timezone.utc) + datetime.timedelta(seconds=300)})}
#
#
# @auth.get('/guest')
# async def about_me(current_user: dict = Depends(get_user_from_token)):
#     if current_user['role'] == 'guest':
#         return {'message': 'Welcome guest(U are not auth)'}
#
#
# @auth.get('/protected_resource')
# async def filter_us(current_user: dict = Depends(get_user_from_token)):
#     print(current_user)
#     if current_user['role'] == 'admin' or current_user == 'user':
#         return {1: current_user}
#     elif current_user['role'] == 'guest':
#         raise InvalidRoleException()
