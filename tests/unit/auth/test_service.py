from datetime import timedelta

import pytest
from fastapi import HTTPException
from jose import jwt

from src.auth.config import get_auth_settings
from src.auth.routers import create_access_token, get_current_user

settings = get_auth_settings()


def test_create_access_token():
    username = "testuser"
    user_id = 1
    email = "testemail@gmail.com"
    expires_delta = timedelta(days=1)

    token = create_access_token(username, user_id, email, expires_delta)

    decoded_token = jwt.decode(
        token,
        settings.secret_key,
        algorithms=[settings.algorithm],
        options={"verify_signature": False},
    )

    assert decoded_token["sub"] == username
    assert decoded_token["id"] == user_id
    assert decoded_token["email"] == email


async def test_get_current_user_valid_token():
    encode = {"sub": "testuser", "id": 1, "email": "testemail@gmail.com"}
    token = jwt.encode(encode, settings.secret_key, algorithm=settings.algorithm)

    user = await get_current_user(token=token)
    assert user.model_dump() == {
        "username": "testuser",
        "id": 1,
        "email": "testemail@gmail.com",
    }


async def test_get_current_user_missing_payload():
    encode = {"role": "user"}
    token = jwt.encode(encode, settings.secret_key, algorithm=settings.algorithm)

    with pytest.raises(HTTPException) as excinfo:
        await get_current_user(token=token)

    assert excinfo.value.status_code == 401
    assert excinfo.value.detail == "Could not validate user."
