import jwt
import uvicorn as uvicorn
from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from auth.exceptions import inv_token
# from src.exceptions import handler_422
from src.ai_chat.router import chat_router
from src.auth.router import auth_router
from src.notes.router import memo_router

memo_app = FastAPI()
memo_app.mount('/static', StaticFiles(directory='../static'), name='static')
memo_app.include_router(auth_router, prefix='/auth')
memo_app.include_router(memo_router, prefix='')
memo_app.include_router(chat_router, prefix='')
memo_app.add_exception_handler(jwt.InvalidTokenError, inv_token)
memo_app.add_exception_handler(jwt.ExpiredSignatureError, inv_token)
memo_app.add_exception_handler(jwt.DecodeError, inv_token)
# memo_app.add_exception_handler(422, handler_422)!

if __name__ == '__main__':
    uvicorn.run('main:memo_app', host='127.0.0.1', port=8000, reload=True)
