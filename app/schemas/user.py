from pydantic import BaseModel


class UserCreateSchema(BaseModel):
    email: str
    password: str
    first_name: str
    last_name: str


class UserSchema(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str

    class Config:
        from_attributes = True
