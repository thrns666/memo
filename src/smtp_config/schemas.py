from pydantic import BaseModel, EmailStr


class VerifyCodeRequest(BaseModel):
    email: EmailStr
    code: str
