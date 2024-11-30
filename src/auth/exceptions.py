from starlette import status
from starlette.requests import Request

from src.auth.router import templates


async def inv_token(request: Request, exc):
    return templates.TemplateResponse(
        request=request,
        name='error_page.html',
        context={'detail': 401},
        status_code=status.HTTP_401_UNAUTHORIZED
    )
