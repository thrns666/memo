from fastapi import APIRouter, Depends, Form
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.requests import Request
from starlette.templating import Jinja2Templates

from postgres_config.database import get_async_session
from src.auth.utils import get_user_from_token
from src.notes.schemas import NoteDataForm, NoteData
from src.postgres_config.dao import NoteDAO

memo_router = APIRouter()
templates = Jinja2Templates(directory='../static/templates')


@memo_router.get('/')
async def get_home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name='home_page.html',
        status_code=status.HTTP_200_OK,
    )


@memo_router.get('/user')
async def get_user_page(request: Request, user: dict = Depends(get_user_from_token)):
    return templates.TemplateResponse(
        request=request,
        name='index_page.html',
        status_code=status.HTTP_200_OK,
    )


@memo_router.get('/create_note')
async def get_create_note(request: Request, user: dict = Depends(get_user_from_token)):
    return templates.TemplateResponse(
        request=request,
        name='create_note_page.html',
        status_code=status.HTTP_200_OK,
    )


@memo_router.post('/create_note')
async def post_create_note(
        request: Request,
        user: dict = Depends(get_user_from_token),
        note_data: NoteDataForm = Form(),
        session: AsyncSession = Depends(get_async_session)
):
    data = NoteData(
        title=note_data.title,
        text=note_data.text,
        owner_email=user['email']
    )
    try:
        await NoteDAO.create_note(note_data=data, session=session)

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


@memo_router.get('/note')
async def get_all_notes_by_user(
        request: Request,
        user: dict = Depends(get_user_from_token),
        session: AsyncSession = Depends(get_async_session)
):
    user_email = user['email']
    try:
        res = await NoteDAO.get_all_notes_by_email(user_email=user_email, session=session)

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


@memo_router.get('/note/{note_id}')
async def get_note_by_id(
        request: Request,
        note_id: int,
        user: dict = Depends(get_user_from_token),
        session: AsyncSession = Depends(get_async_session)
):
    try:
        res = await NoteDAO.get_one_or_none(id=note_id, session=session)

        if not res:
            return templates.TemplateResponse(
                request=request,
                name='index_page.html',
                context={'result': 'Note with this id does not exist'},
                status_code=status.HTTP_404_NOT_FOUND
            )

        return templates.TemplateResponse(
            request=request,
            name='view_note_page.html',
            context={'note': res, 'user': user['email']},
            status_code=status.HTTP_200_OK
        )
    except Exception as ex:
        logger.error(f'Error in get_note_by_id: {ex}')

        return templates.TemplateResponse(
            request=request,
            name='error_page.html',
            context={'detail': ex},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
