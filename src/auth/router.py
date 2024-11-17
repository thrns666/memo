import datetime
import traceback

from fastapi import APIRouter, HTTPException, Depends, Form
from loguru import logger
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.requests import Request
from starlette.responses import RedirectResponse, HTMLResponse
from starlette.templating import Jinja2Templates

from postgres_config.database import get_async_session
from src.celery_config.tasks import send_mail_with_pass, send_acceptance_mail
from src.auth.schemas import LoginUser, RegisterUser
from src.auth.utils import create_jwt_token, get_user_from_token
from src.postgres_config.dao import UserDAO
from src.redis_config.crud import get_session

auth_router = APIRouter()
templates = Jinja2Templates(directory='../static/templates')


@auth_router.get('/login', response_class=HTMLResponse)
async def get_login(request: Request):
    return templates.TemplateResponse(request=request, name='login_page.html', status_code=status.HTTP_200_OK)


@auth_router.post('/login')
async def post_login(request: Request, email: EmailStr = Form(), session: AsyncSession = Depends(get_async_session)):
    try:
        user = await UserDAO.get_one_or_none(session=session, email=email)
        if not user:
            logger.info(f'User {email} not found')
            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User not found')

        send_mail_with_pass.apply_async(args=[email])
        url = request.url_for('post_password')
        return RedirectResponse(url=f'{url}?email={email}', status_code=status.HTTP_308_PERMANENT_REDIRECT)
    except Exception as ex:
        # tb = traceback.format_exc()
        logger.error(f'Error in login user: {ex}')

        return templates.TemplateResponse(
            request=request,
            name='error_page.html',
            context={'detail': ex},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@auth_router.post('/password')
async def post_password(request: Request, email: EmailStr):
    return templates.TemplateResponse(
        request=request,
        name='login_page.html',
        context={'user_email': f'{email}'},
        status_code=status.HTTP_200_OK,
    )


@auth_router.post('/check_password')
async def post_check_password(request: Request, user_data: LoginUser = Form()):
    try:
        res: bytes = await get_session(user_data.email)
        if not res:
            return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='No database matches')
        elif res.decode != user_data.password:
            return templates.TemplateResponse(
                request=request,
                status_code=status.HTTP_204_NO_CONTENT,
                name='login_page.html',
                context={'result': f'Wrong password', 'user_email': user_data.email}
            )

        value = create_jwt_token(
            {
                'sub': {
                    'email': user_data.email,
                },
                'exp': datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(seconds=3000)
            }
        )

        response = templates.TemplateResponse(
            request=request,
            name='succss_login.html',
            context={'exmp': 'test successful login'},
            status_code=status.HTTP_302_FOUND,
        )
        response.set_cookie('auth_token', value, expires=3000)
        return response
    except Exception as ex:
        tb = traceback.format_exc()
        logger.error(f'Error in check_password: {ex}---{tb}')

        return templates.TemplateResponse(
            request=request,
            name='error_page.html',
            context={'detail': ex},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@auth_router.get('/create_user')
async def get_create_user(request: Request):
    return templates.TemplateResponse(
        request=request,
        name='create_user_page.html',
        status_code=status.HTTP_200_OK
    )


@auth_router.post('/create_user')
async def post_create_user(
        request: Request,
        data: RegisterUser = Form(),
        session: AsyncSession = Depends(get_async_session)
):
    try:
        await UserDAO.create_user(user_data=data, session=session)
        send_acceptance_mail.apply_async(args=[data.email])

        return templates.TemplateResponse(
            request=request,
            name='succss_login.html',
            status_code=status.HTTP_201_CREATED
        )
    except Exception as ex:
        tb = traceback.format_exc()
        return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'{ex}')


@auth_router.get('/help')
async def filter_us(
        request: Request,
        session: AsyncSession = Depends(get_async_session)
):
    return 'ok'
