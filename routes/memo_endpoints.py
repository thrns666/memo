from fastapi import APIRouter, Depends, Form
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
        name='index_page.html',
        status_code=status.HTTP_200_OK,
    )

!!!!!!!!!!!! NEED MIGRATION TO POSTGRES, IM !!!!EDIT OWNER_ID TO OWNER_EMAIL !!!!

@memo_router.post('/create_note')
async def post_create_note(request: Request, user: dict = Depends(get_user_from_token), note_data: str = Form()):
    if not user:
        return
    dat = NoteData(text=note_data, owner_email=user['sub']['email'])
    try:
        await NoteDAO.create_note(text=note_data)

        return templates.TemplateResponse(
            request=request,
            name='index_page.html',
            context={'result': 'Note created'},
            status_code=status.HTTP_200_OK,
        )
    except Exception as ex:
        return ex
