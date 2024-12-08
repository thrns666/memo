from fastapi import HTTPException
from starlette import status
from starlette.requests import Request

from src.auth.router import templates


async def handler_422(request: Request, exc: HTTPException):
    await templates.TemplateResponse(
        request=request,
        name='error_page.html',
        context={'detail': exc},
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
    )
