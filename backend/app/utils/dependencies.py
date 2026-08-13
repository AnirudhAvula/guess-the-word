from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from bson import ObjectId

from app.config import settings
from app.database import users_collection


security = HTTPBearer()


# ==================================================
# GET CURRENT USER
# ==================================================

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials

    # ----------------------------------------------
    # Decode JWT
    # ----------------------------------------------

    try:

        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM]
        )

        user_id = payload.get("sub")

        if not user_id:

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication token"
            )

    except JWTError:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

    # ----------------------------------------------
    # Find user in MongoDB
    # ----------------------------------------------

    try:

        user = users_collection.find_one(
            {"_id": ObjectId(user_id)}
        )

    except Exception:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user ID"
        )

    if not user:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    return user


# ==================================================
# PLAYER ACCESS
# ==================================================

def get_current_player(
    current_user=Depends(get_current_user)
):

    if current_user["role"] != "PLAYER":

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Player access required"
        )

    return current_user


# ==================================================
# ADMIN ACCESS
# ==================================================

def get_current_admin(
    current_user=Depends(get_current_user)
):

    if current_user["role"] != "ADMIN":

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )

    return current_user