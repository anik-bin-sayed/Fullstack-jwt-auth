from jose import JWTError

from fastapi import APIRouter, Response, Depends, HTTPException, Request

from app.schemas.user import *
from app.database.mongodb import user_collection
from app.dependencies.auth import get_current_user
from app.utils.password import hashed_password, verify_password
from app.services.auth_service import get_user_by_email, create_user
from app.utils.jwt import create_access_token, create_refresh_token, decode_token

router = APIRouter()


@router.post("/register")
async def register(data: RegisterSchema):
    user = await get_user_by_email(data.email)

    if user:
        raise HTTPException(400, "User already exists")

    data = {
        "name": data.name,
        "email": data.email,
        "password": hashed_password(data.password),
    }
    await create_user(data)

    return {"message": "Registered"}


@router.post("/login")
async def login(data: LoginSchema, response: Response):
    user = await get_user_by_email(data.email)

    print(user["_id"])

    if not user:
        raise HTTPException(401, "Invalid Credentials")

    password_verify = verify_password(data.password, user["password"])

    if not password_verify:
        raise HTTPException(401, "Invalid credentials")

    access_token = create_access_token({"email": user["email"]})
    refresh_token = create_refresh_token({"email": user["email"]})

    response.set_cookie(
        key="access_token", value=access_token, httponly=True, samesite="lax"
    )

    response.set_cookie(
        key="refresh_token", value=refresh_token, httponly=True, samesite="lax"
    )

    return {"message": "Login Success"}


@router.post("/logout")
async def logout(response: Response, user=Depends(get_current_user)):
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")

    return {"message": "Logout Success"}


@router.post("/refresh")
async def refresh(request: Request, response: Response):
    refresh_token = request.cookies.get("refresh_token")

    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token is missing")

    try:
        payload = decode_token(token=refresh_token)
        print(payload)
        if payload["type"] != "refresh":
            raise HTTPException(status_code=401, detail="invalid token")

        new_access_token = create_access_token({"email": payload["email"]})

        response.set_cookie(
            key="access_token", value=new_access_token, httponly=True, samesite="lax"
        )

        return {"message": "Token refreshed"}

    except JWTError:
        raise HTTPException(status_code=401, detail="invalid refresh token")


@router.get("/me")
async def me(user=Depends(get_current_user)):

    return {"id": str(user["_id"]), "name": user["name"], "email": user["email"]}
