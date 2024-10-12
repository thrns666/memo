from fastapi import APIRouter, Depends, Form
from loguru import logger
from starlette import status
from starlette.requests import Request
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates

from postgre_db.dao import NoteDAO
from postgre_db.schemas import NoteData
from routes.auth import get_user_from_token

memo_router = APIRouter()
templates = Jinja2Templates(directory='static/templates')


@memo_router.get('/')
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name='home_page.html',
        status_code=status.HTTP_200_OK,
    )


@memo_router.get('/index')
async def index(request: Request, current_user: dict = Depends(get_user_from_token)):
    if not current_user:
        url = request.url_for('home')
        return RedirectResponse(url=url, status_code=status.HTTP_401_UNAUTHORIZED)

    return templates.TemplateResponse(
        request=request,
        name='index_page.html',
        status_code=status.HTTP_200_OK,
    )


@memo_router.get('/create_note')
async def get_create_note(request: Request, user: dict = Depends(get_user_from_token)):
    if not user:
        return

    return templates.TemplateResponse(
        request=request,
        name='create_note_page.html',
        status_code=status.HTTP_200_OK,
    )


@memo_router.get('/all_notes/{note_id}')
async def get_note_by_id(request: Request, note_id: int, user: dict = Depends(get_user_from_token)):
    if not user:
        return

    try:
        res = await NoteDAO.get_one_or_none(id=note_id)

        if res:
            return templates.TemplateResponse(
                request=request,
                name='view_note_page.html',
                context={'note': res, 'user': user['email']}
            )
    except Exception as ex:
        logger.error(f'Error in get_note_by_id: {ex}')

        return templates.TemplateResponse(
            request=request,
            name='error_page.html',
            context={'detail': ex},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@memo_router.post('/create_note')
async def post_create_note(request: Request, user: dict = Depends(get_user_from_token), title: str = Form(), text: str = Form()):
    if not user:
        return
    dat = NoteData(title=title, text=text, owner_email=user['email'])
    try:
        await NoteDAO.create_note(dat)

        return templates.TemplateResponse(
            request=request,
            name='index_page.html',
            context={'result': 'Note created'},
            status_code=status.HTTP_200_OK,
        )
    except Exception as ex:
        return templates.TemplateResponse(
            request=request,
            name='error_page.html',
            context={'detail': ex},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@memo_router.get('/all_notes')
async def get_all_notes_by_user(request: Request, user: dict = Depends(get_user_from_token)):
    user_email = user['email']
    try:
        res = await NoteDAO.get_all_notes_by_email(user_email)

        return templates.TemplateResponse(
            request=request,
            name='index_page.html',
            context={
                'result': f'{user_email} Notes',
                'notes': res
            },
            status_code=status.HTTP_200_OK,
        )
    except Exception as ex:
        logger.error(f'Error in get all notes by user: {ex}')

        return templates.TemplateResponse(
            request=request,
            name='error_page.html',
            context={'detail': ex},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
