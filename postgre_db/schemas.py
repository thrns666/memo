from pydantic import BaseModel, EmailStr


class LoginUser(BaseModel):
    email: EmailStr


class RegisterUser(BaseModel):
    username: str
    email: EmailStr


class NoteDataForm(BaseModel):
    title: str
    text: str


class NoteData(BaseModel):
    title: str
    text: str
    owner_email: EmailStr


class VerifyCodeRequest(BaseModel):
    email: EmailStr
    code: str
