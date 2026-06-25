from app.database.mongodb import user_collection


async def get_user_by_email(email: str):
    return await user_collection.find_one({"email": email})


async def create_user(data):
    return await user_collection.insert_one(data)
