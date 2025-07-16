from pydantic import BaseModel, Field


class UserLogin(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)


class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)


class UserRead(BaseModel):
    id: str
    username: str

    class Config:
        from_attributes = True  # для pydantic v2


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
