from pydantic import EmailStr, BaseModel


class LoginUser(BaseModel):
    email: EmailStr


class RegisterUser(BaseModel):
    username: str
    email: EmailStr
