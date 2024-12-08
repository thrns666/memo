import base64

from fastapi import APIRouter, Depends, Form, Cookie, HTTPException
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.templating import Jinja2Templates

from src.auth.utils import get_user_from_token
from src.notes.models import Note
from src.notes.schemas import NoteDataForm, NoteData
from src.notes.utils import create_share_link
from src.postgres_config.dao import NoteDAO
from src.postgres_config.database import get_async_session

memo_router = APIRouter()
templates = Jinja2Templates(directory='../static/templates')


@memo_router.get('/')
async def get_home(request: Request, auth_token: str = Cookie(default=None)):
    return templates.TemplateResponse(
        request=request,
        name='home_page.html',
        status_code=status.HTTP_200_OK,
        context={'user': auth_token}
    )


@memo_router.get('/user')
async def get_user_page(request: Request, user: dict = Depends(get_user_from_token)):
    return templates.TemplateResponse(
        request=request,
        name='index_page.html',
        status_code=status.HTTP_200_OK,
        context={'user': user.get('email')}
    )


@memo_router.get('/create_note')
async def get_create_note(request: Request, user: dict = Depends(get_user_from_token)):
    return templates.TemplateResponse(
        request=request,
        name='create_note_page.html',
        status_code=status.HTTP_200_OK,
        context={'user': user.get('email')}
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
        owner_email=user.get('email')
    )
    try:
        await NoteDAO.create_note(note_data=data, session=session)

        return templates.TemplateResponse(
            request=request,
            name='index_page.html',
            context={'result': 'Note created', 'user': user.get('email')},
            status_code=status.HTTP_200_OK,
        )
    except Exception as ex:
        return templates.TemplateResponse(
            request=request,
            name='error_page.html',
            context={'detail': ex, 'user': user.get('email')},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@memo_router.get('/notes')
async def get_all_notes_by_user(
        request: Request,
        user: dict = Depends(get_user_from_token),
        session: AsyncSession = Depends(get_async_session)
):
    user_email = user.get('email')
    try:
        res = await NoteDAO.get_all_notes_by_email(user_email=user_email, session=session)

        return templates.TemplateResponse(
            request=request,
            name='index_page.html',
            context={
                'notes': res,
                'user': user_email,
                'username': user.get('username')
            },
            status_code=status.HTTP_200_OK,
        )
    except Exception as ex:
        logger.error(f'Error in get all notes by user: {ex}')

        return templates.TemplateResponse(
            request=request,
            name='error_page.html',
            context={'detail': ex, 'user': user.get('email')},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@memo_router.get('/notes/{note_id}')
async def get_note_by_id(
        request: Request,
        note_id: int,
        user: dict = Depends(get_user_from_token),
        session: AsyncSession = Depends(get_async_session)
):
    try:
        res: Note = await NoteDAO.get_one_or_none(id=note_id, session=session)

        if res and user.get('email') != res.owner_email:
            return templates.TemplateResponse(
                request=request,
                name='index_page.html',
                context={'result': 'This user dont have notes with this id', 'user': user.get('email')},
                status_code=status.HTTP_403_FORBIDDEN
            )
        elif not res:
            return templates.TemplateResponse(
                request=request,
                name='index_page.html',
                context={'result': 'Note with this id does not exist', 'user': user.get('email')},
                status_code=status.HTTP_404_NOT_FOUND
            )

        return templates.TemplateResponse(
            request=request,
            name='view_note_page.html',
            context={'note': res, 'user': user.get('email')},
            status_code=status.HTTP_200_OK
        )
    except Exception as ex:
        logger.error(f'Error in get_note_by_id: {ex}')

        return templates.TemplateResponse(
            request=request,
            name='error_page.html',
            context={'detail': ex, 'user': user.get('email')},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@memo_router.get('/{share_note}')
async def get_shared_note(
        request: Request,
        share_note: str,
        session: AsyncSession = Depends(get_async_session),
        auth_token: str = Cookie(default=None)
):
    try:
        data = base64.b64decode(share_note)
        data = data.decode('UTF-8')
        owner_email, note_id = data.split('+')

        res = await NoteDAO.get_one_or_none(session=session, owner_email=owner_email, id=int(note_id))

        return templates.TemplateResponse(
            request=request,
            name='view_note_page.html',
            context={'note': res, 'user': auth_token},
            status_code=status.HTTP_200_OK
        )
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=ex)


@memo_router.get('/notes/{note_id}/create_share_link_for_note')
async def get_create_share_link(
        note_id: int,
        user: dict = Depends(get_user_from_token),
        session: AsyncSession = Depends(get_async_session)
):
    try:
        res: Note = await NoteDAO.get_one_or_none(id=note_id, session=session)

        if res and user.get('email') != res.owner_email:
            return HTTPException(
                detail='This user dont have notes with this id',
                status_code=status.HTTP_403_FORBIDDEN
            )
        elif not res:
            return HTTPException(
                detail='Note with this id does not exist',
                status_code=status.HTTP_404_NOT_FOUND
            )
        elif res:
            link_json = await create_share_link(note=res, url='127.0.0.1:8000')

            return JSONResponse(
                content=link_json,
                status_code=status.HTTP_200_OK,
                media_type='application/json'
            )

        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Try again')

    except Exception as ex:
        return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'{ex}')

# Need: - realize editing user notes, change encoding from base64 → JWT with expiry date
# Celery tasks for send email: set max retry - 2 times
