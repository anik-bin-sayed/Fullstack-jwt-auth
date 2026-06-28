from motor.motor_asyncio import AsyncIOMotorClient
from app.config.settings import settings

client = AsyncIOMotorClient(settings.MONGO_URL)

db = client[settings.DATABASE_NAME]

user_collection = db.users
refresh_tokens_collection = db["refresh_tokens"]
