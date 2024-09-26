from pydantic import BaseModel, EmailStr


class RedisLoginData(BaseModel):
    email: EmailStr
    user_password: int
