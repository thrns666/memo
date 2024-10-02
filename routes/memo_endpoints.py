import traceback
from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse
from postgre_db.dao import UserDAO

memo_router = APIRouter()


@memo_router.get('/')
async def home(request: Request):
    print(request.headers)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content='200 ok app is running')


@memo_router.get('/index')
async def index():
    try:
        all_notes = await UserDAO.get_all()
    except Exception as ex:
        tb = traceback.format_exc()
        return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={'err': ex, 'traceback': tb})
    return JSONResponse(status_code=status.HTTP_200_OK, content=all_notes)
