import jwt
from starlette import status
from starlette.requests import Request

# from main import memo_app
from src.auth.router import templates


# @memo_app.exception_handler(jwt.InvalidTokenError, jwt.ExpiredSignatureError)
async def inv_token(request: Request, exc):
    return templates.TemplateResponse(
        request=request,
        name='error_page.html',
        context={'detail': 401},
        status_code=status.HTTP_401_UNAUTHORIZED
    )
