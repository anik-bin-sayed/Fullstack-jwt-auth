from fastapi import Request, HTTPException

from jose import jwt

from app.config.settings import settings
from app.database.mongodb import user_collection


async def get_current_user(request: Request):
    token = request.cookies.get("access_token")

    if not token:
        raise HTTPException(401, "Unauthorized")

    payload = jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])

    email = payload["email"]

    user = await user_collection.find_one({"email": email})

    if not user:
        raise HTTPException(404, "User not found")

    return user
