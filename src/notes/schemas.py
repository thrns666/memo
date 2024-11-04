from pydantic import BaseModel, EmailStr


class NoteDataForm(BaseModel):
    title: str
    text: str


class NoteData(BaseModel):
    title: str
    text: str
    owner_email: EmailStr
