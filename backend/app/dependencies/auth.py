from fastapi import Request, HTTPException

from jose import jwt
from datetime import datetime
from app.config.settings import settings
from app.database.mongodb import user_collection
from app.database.mongodb import refresh_tokens_collection


async def get_current_user(request: Request):
    token = request.cookies.get("access_token")

    if not token:
        raise HTTPException(401, "Unauthorized")

    payload = jwt.decode(
        token,
        settings.SECRET_KEY or settings.JWT_SECRET,
        algorithms=[settings.ALGORITHM or "HS256"],
    )

    email = payload["email"]

    user = await user_collection.find_one({"email": email})

    if not user:
        raise HTTPException(404, "User not found")

    return user


async def save_refresh_token_record(
    user_id: str,
    jti: str,
    revoked,
):
    await refresh_tokens_collection.insert_one(
        {
            "user_id": user_id,
            "jti": jti,
            "revoked": revoked,
            "created_at": datetime.utcnow(),
        }
    )
