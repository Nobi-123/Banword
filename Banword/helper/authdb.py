from Banword.helper.database import db

async def add_auth_user(chat_id, user_id):
    await db.auth.update_one(
        {"chat_id": chat_id},
        {"$addToSet": {"users": user_id}},
        upsert=True
    )

async def remove_auth_user(chat_id, user_id):
    await db.auth.update_one(
        {"chat_id": chat_id},
        {"$pull": {"users": user_id}}
    )

async def get_auth_users(chat_id):
    doc = await db.auth.find_one({"chat_id": chat_id})
    return doc["users"] if doc and "users" in doc else []
