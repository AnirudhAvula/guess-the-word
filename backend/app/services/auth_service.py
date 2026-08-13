from datetime import datetime, timezone

from app.database import users_collection
from app.utils.jwt import create_access_token
from app.utils.security import (
    hash_password,
    verify_password
)


def register_user(
    username: str,
    password: str
):

    existing_user = users_collection.find_one(
        {"username": username}
    )

    if existing_user:
        raise ValueError(
            "Username already exists"
        )

    user = {
        "username": username,
        "password_hash": hash_password(password),
        "role": "PLAYER",
        "created_at": datetime.now(timezone.utc)
    }

    result = users_collection.insert_one(user)

    return {
        "id": str(result.inserted_id),
        "username": username,
        "role": "PLAYER"
    }


def login_user(
    username: str,
    password: str
):

    user = users_collection.find_one(
        {"username": username}
    )

    if not user:
        raise ValueError(
            "Invalid username or password"
        )

    if not verify_password(
        password,
        user["password_hash"]
    ):
        raise ValueError(
            "Invalid username or password"
        )

    token = create_access_token(
        user_id=str(user["_id"]),
        role=user["role"]
    )

    return {
    "access_token": token,
    "token_type": "bearer",
    "role": user["role"],
    "username": user["username"]
}