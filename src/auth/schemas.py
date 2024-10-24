from pydantic import BaseModel


class CreateUserRequest(BaseModel):
    # TODO: Add email and password validations
    username: str
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class DecodedToken(BaseModel):
    id: int
    username: str
    email: str
