from datetime import timedelta
from fastapi import HTTPException
import pytest
from src.auth.routers import create_access_token, get_current_user
from jose import jwt


SECRET_KEY = "197b2c37c391bed93fe80344fe73b806947a65e36206e05a1a23c2fa12702fe3"
ALGORITHM = "HS256"


def test_create_access_token():
    username = "testuser"
    user_id = 1
    email = "testemail@gmail.com"
    expires_delta = timedelta(days=1)

    token = create_access_token(username, user_id, email, expires_delta)

    decoded_token = jwt.decode(
        token, SECRET_KEY, algorithms=[ALGORITHM], options={"verify_signature": False}
    )

    assert decoded_token["sub"] == username
    assert decoded_token["id"] == user_id
    assert decoded_token["email"] == email


async def test_get_current_user_valid_token():
    encode = {"sub": "testuser", "id": 1, "email": "testemail@gmail.com"}
    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

    user = await get_current_user(token=token)
    assert user.model_dump() == {"username": "testuser", "id": 1, "email": "testemail@gmail.com"}


async def test_get_current_user_missing_payload():
    encode = {"role": "user"}
    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

    with pytest.raises(HTTPException) as excinfo:
        await get_current_user(token=token)

    assert excinfo.value.status_code == 401
    assert excinfo.value.detail == "Could not validate user."
