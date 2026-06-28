import uuid

from jose import JWTError

from fastapi import APIRouter, Response, Depends, HTTPException, Request

from app.schemas.user import *
from app.database.mongodb import user_collection
from app.dependencies.auth import get_current_user, save_refresh_token_record
from app.utils.password import hashed_password, verify_password
from app.services.auth_service import (
    get_user_by_email,
    create_user,
    get_refresh_token_record,
    revoke_all_tokens_for_user,
    revoke_refresh_token_record,
)
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

    if not user:
        raise HTTPException(401, "Invalid Credentials")

    password_verify = verify_password(data.password, user["password"])

    if not password_verify:
        raise HTTPException(401, "Invalid credentials")

    jti = str(uuid.uuid4())
    access_token = create_access_token({"email": user["email"]})
    refresh_token = create_refresh_token({"email": user["email"]}, jti=jti)

    await save_refresh_token_record(user_id=user["_id"], jti=jti, revoked=False)

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        samesite="lax",
        max_age=15 * 60,
    )

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        samesite="lax",
        max_age=7 * 24 * 60 * 60,
    )

    return {"message": "Login Success"}


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

        jti = payload["jti"]

        db_record = await get_refresh_token_record(jti=jti)

        if db_record is None or db_record["revoked"]:
            await revoke_all_tokens_for_user(user_id)
            raise HTTPException(401, "Session invalid, please log in again")

        user_id = db_record["user_id"]

        await revoke_refresh_token_record(jti)
        new_jti = str(uuid.uuid4())
        new_access_token = create_access_token({"email": payload["email"]})
        new_refresh_token = create_refresh_token(
            {"email": payload["email"]}, jti=new_jti
        )
        await save_refresh_token_record(user_id=user_id, jti=new_jti, revoked=False)

        response.set_cookie(
            key="access_token",
            value=new_access_token,
            httponly=True,
            samesite="lax",
            max_age=15 * 60,
        )

        response.set_cookie(
            key="refresh_token",
            value=new_refresh_token,
            httponly=True,
            # secure=True,
            samesite="lax",
            max_age=7 * 24 * 60 * 60,
        )

        return {"message": "Token refreshed"}

    except JWTError:
        raise HTTPException(status_code=401, detail="invalid refresh token")


@router.get("/me")
async def me(user=Depends(get_current_user)):

    return {"id": str(user["_id"]), "name": user["name"], "email": user["email"]}


@router.post("/logout")
async def logout(request: Request, response: Response):
    token = request.cookies.get("refresh_token")
    if token:
        try:
            payload = decode_token(token=token)
            await revoke_refresh_token_record(payload["jti"])
        except JWTError:
            pass

    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")

    return {"message": "Logout Success"}
