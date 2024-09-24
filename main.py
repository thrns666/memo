import uvicorn as uvicorn
from fastapi import FastAPI
from starlette.staticfiles import StaticFiles
from routes.auth import auth_router
from routes.memo_endpoints import memo_router

memo_app = FastAPI()
memo_app.mount('/static', StaticFiles(directory='static'), name='static')
memo_app.include_router(auth_router, prefix='/auth')
memo_app.include_router(memo_router, prefix='')


if __name__ == '__main__':
    uvicorn.run('main:memo_app', host='127.0.0.1', port=8000)
