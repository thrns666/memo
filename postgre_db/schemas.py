from pydantic import BaseModel, EmailStr


class LoginUser(BaseModel):
    email: EmailStr


class RegisterUser(BaseModel):
    name: str
    email: EmailStr


class Note(BaseModel):
    text: str
    owner_id: int


class VerifyCodeRequest(BaseModel):
    email: EmailStr
    code: str
