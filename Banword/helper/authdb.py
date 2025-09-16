from Banword.helper.database import db

# Collection name (MongoDB style; if you're using another DB adjust accordingly)
auth_col = db.auth_users

async def add_auth_user(chat_id: int, user_id: int):
    """Add a user as authorized in a specific chat."""
    existing = await auth_col.find_one({"chat_id": chat_id, "user_id": user_id})
    if not existing:
        await auth_col.insert_one({"chat_id": chat_id, "user_id": user_id})
        return True
    return False

async def is_authorized(chat_id: int, user_id: int) -> bool:
    """Check if user is authorized in this chat."""
    return await auth_col.find_one({"chat_id": chat_id, "user_id": user_id}) is not None

async def get_auth_users(chat_id: int) -> list:
    """Return list of authorized user IDs for a chat."""
    cursor = auth_col.find({"chat_id": chat_id})
    return [doc["user_id"] async for doc in cursor]

async def remove_auth_user(chat_id: int, user_id: int):
    """Remove a user from authorized list in a chat."""
    await auth_col.delete_one({"chat_id": chat_id, "user_id": user_id})
