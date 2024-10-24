from datetime import timedelta, datetime, timezone
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status
from .repository import UserRepository
from .service import UserService
from src.auth.models import User
from src.auth.schemas import CreateUserRequest, DecodedToken, Token
from src.adapters.database import get_db
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError

router = APIRouter(prefix="/auth", tags=["auth"])

SECRET_KEY = "197b2c37c391bed93fe80344fe73b806947a65e36206e05a1a23c2fa12702fe3"
ALGORITHM = "HS256"

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")


db_dependency = Annotated[Session, Depends(get_db)]


def get_user_repository(session: db_dependency):
    return UserRepository(session)


repository = Annotated[UserRepository, Depends(get_user_repository)]


def get_user_service(repo: repository):
    return UserService(repo)


user_service = Annotated[UserService, Depends(get_user_service)]


def create_access_token(
    username: str, user_id: int, email: str, expires_delta: timedelta
):
    encode = {"sub": username, "id": user_id, "email": email}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({"exp": expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(
    token: Annotated[str, Depends(oauth2_bearer)]
) -> DecodedToken:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub", None)
        user_id: int = payload.get("id", None)
        user_email: str = payload.get("email", None)
        if username is None or user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate user.",
            )
        return DecodedToken(id=user_id, username=username, email=user_email)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user."
        )


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(repo: repository, create_user_request: CreateUserRequest):
    create_user_model = User(
        username=create_user_request.username,
        email=create_user_request.email,
        password=bcrypt_context.hash(create_user_request.password),
    )
    new_user = create_user_request.model_copy()
    new_user.password = bcrypt_context.hash(new_user.password)
    await repo.create_user(new_user.model_dump())
    # db.add(create_user_model)
    # db.commit()


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], service: user_service
):
    user = await service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user."
        )
    token = create_access_token(
        user.username, user.id, user.email, timedelta(minutes=20)
    )

    return {"access_token": token, "token_type": "bearer"}
