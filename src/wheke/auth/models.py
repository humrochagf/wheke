from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str


class User(BaseModel):
    username: str
    email: EmailStr
    full_name: str
    disabled: bool = False


class UserInDB(User):
    hashed_password: str
