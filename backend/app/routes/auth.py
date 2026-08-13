from fastapi import APIRouter, HTTPException, status
from fastapi import Depends
from app.utils.dependencies import get_current_user

from app.schemas.auth import (
    LoginRequest,
    RegisterRequest,
    TokenResponse
)

from app.services.auth_service import (
    login_user,
    register_user
)

from app.utils.validators import (
    validate_password,
    validate_username
)


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED
)
def register(request: RegisterRequest):

    if not validate_username(
        request.username
    ):
        raise HTTPException(
            status_code=400,
            detail=(
                "Username must contain at least "
                "5 letters and only alphabetic "
                "characters."
            )
        )

    if not validate_password(
        request.password
    ):
        raise HTTPException(
            status_code=400,
            detail=(
                "Password must be at least 5 "
                "characters and contain an "
                "alphabet, number, and one of "
                "$, %, *."
            )
        )

    try:

        return register_user(
            request.username,
            request.password
        )

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@router.post(
    "/login",
    response_model=TokenResponse
)
def login(request: LoginRequest):

    try:

        return login_user(
            request.username,
            request.password
        )

    except ValueError as e:

        raise HTTPException(
            status_code=401,
            detail=str(e)
        )

@router.get("/me")
def get_me(
    current_user=Depends(get_current_user)
):
    return {
        "id": str(current_user["_id"]),
        "username": current_user["username"],
        "role": current_user["role"]
    }