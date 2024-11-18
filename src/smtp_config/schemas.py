from pydantic import (
    BaseModel,
    ValidationError,
    ValidationInfo,
    field_validator,
    EmailStr,
)


class VerifyCodeRequest(BaseModel):
    email: EmailStr
    code: str

    @field_validator('code')
    @classmethod
    def code_valid(cls, code: str) -> str:
        if code.isdigit() and len(code) == 6:
            return code
        else:
            raise ValueError('Code is six digits, example: 012345')
