from pydantic import EmailStr, BaseModel


class LoginUser(BaseModel):
    email: EmailStr
    password: int


class RegisterUser(BaseModel):
    username: str
    email: EmailStr
