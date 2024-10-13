import datetime
import traceback

import jwt
from fastapi import APIRouter, HTTPException, Depends, Form
from fastapi.security import OAuth2PasswordBearer
from loguru import logger
from pydantic import EmailStr
from starlette import status
from starlette.requests import Request
from starlette.responses import RedirectResponse, HTMLResponse
from starlette.templating import Jinja2Templates

from celery_config.tasks import send_mail_with_pass, send_acceptance_mail
from postgre_db.dao import UserDAO
from postgre_db.schemas import LoginUser, RegisterUser
from redis_config.redis_crud import get_session

auth_router = APIRouter()
templates = Jinja2Templates(directory='static/templates')

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')
SECRET_KEY = 'hzcho'
ALGORITHM = 'HS256'


def create_jwt_token(data: dict):
    return jwt.encode(payload=data, key=SECRET_KEY, algorithm=ALGORITHM)


def get_user_from_token(token: str = Depends(oauth2_scheme)):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return payload.get('sub')


async def inv_token(request: Request, exc):
    return templates.TemplateResponse(
        request=request,
        name='error_page.html',
        context={'detail': exc},
        status_code=status.HTTP_401_UNAUTHORIZED
    )


@auth_router.get('/login', response_class=HTMLResponse)
async def login_user(request: Request):
    return templates.TemplateResponse(request=request, name='login_page_0.html', status_code=200)


@auth_router.post('/login', response_class=RedirectResponse)
async def login(request: Request, data: LoginUser = Form()):
    try:
        user = await UserDAO.get_one_or_none(email=data.email)
        if not user:
            logger.info(f'User {data.email} not found')
            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User not found')

        send_mail_with_pass.apply_async(args=[data.email])
        url = request.url_for('get_password')
        return RedirectResponse(url=f'{url}?email={data.email}', status_code=status.HTTP_307_TEMPORARY_REDIRECT)
    except Exception as ex:
        tb = traceback.format_exc()
        logger.error(f'Error in login user: {ex} -- {tb}')
        return HTTPException(status_code=500, detail=ex)


@auth_router.post('/password', response_class=HTMLResponse)
async def get_password(request: Request, email: EmailStr):
    return templates.TemplateResponse(
        request=request,
        name='login_page_1.html',
        context={'user_email': f'{email}'},
        status_code=200,
    )


@auth_router.post('/check_password')
async def check_password(request: Request, email: str = Form(), password: str = Form()):
    try:
        res: bytes = await get_session(email)
        if res.decode() != password:
            return templates.TemplateResponse(
                request=request,
                name='login_page_1.html',
                context={'result': f'Wrong password', 'user_email': email}
            )

        headers = {'access_token': create_jwt_token(
            {
                'sub': {
                    'email': email,
                },
                'exp': datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(seconds=5000)
            }
        ),
            'token_type': 'bearer'}

        return templates.TemplateResponse(
            request=request,
            name='sucss_login.html',
            context={'exmp': 'test successful login'},
            status_code=status.HTTP_302_FOUND,
            headers=headers
        )
    except Exception as ex:
        logger.error(f'Error in check_password: {ex}')

        return templates.TemplateResponse(
            request=request,
            name='error_page.html',
            context={'detail': ex},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@auth_router.get('/protected_resource')
async def filter_us(current_user: dict = Depends(get_user_from_token)):
    print(current_user)
    if current_user:
        return {1: current_user}


@auth_router.get('/create_user')
async def get_create_user(request: Request):
    return templates.TemplateResponse(
        request=request,
        name='create_user_page.html',
        status_code=status.HTTP_200_OK
    )


@auth_router.post('/create_user')
async def create_user(request: Request, data: RegisterUser = Form()):
    try:
        await UserDAO.create_user(data)
        send_acceptance_mail.apply_async(args=[data.email])

        return templates.TemplateResponse(
            request=request,
            name='sucss_login.html',
            status_code=status.HTTP_201_CREATED
        )
    except Exception as ex:
        return templates.TemplateResponse(
            request=request,
            name='create_user_page.html',
            context={'result': ex},
            status_code=status.HTTP_400_BAD_REQUEST
        )

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
