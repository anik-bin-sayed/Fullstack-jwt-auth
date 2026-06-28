from app.database.mongodb import user_collection
from app.database.mongodb import refresh_tokens_collection


async def get_user_by_email(email: str):
    return await user_collection.find_one({"email": email})


async def create_user(data):
    return await user_collection.insert_one(data)


async def get_refresh_token_record(jti: str):
    return await refresh_tokens_collection.find_one({"jti": jti})


async def revoke_all_tokens_for_user(user_id: str):
    await refresh_tokens_collection.update_many(
        {"user_id": user_id}, {"$set": {"revoked": True}}
    )


async def revoke_refresh_token_record(jti: str):
    await refresh_tokens_collection.update_one(
        {"jti": jti}, {"$set": {"revoked": True}}
    )
