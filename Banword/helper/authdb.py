# helper/authdb.py
#
# Database functions for managing authorized users per group.
# Each group (chat_id) has its own list of authorized users.

from Banword.helper.database import db

# Use a collection/table for storing auth users
auth_col = db.auth_users


async def add_auth_user(chat_id: int, user_id: int) -> bool:
    """Add a user to the authorized list of a specific chat."""
    existing = await auth_col.find_one({"chat_id": chat_id, "user_id": user_id})
    if not existing:
        await auth_col.insert_one({"chat_id": chat_id, "user_id": user_id})
        return True
    return False


async def is_authorized(chat_id: int, user_id: int) -> bool:
    """Check if a user is authorized in a given chat."""
    return await auth_col.find_one({"chat_id": chat_id, "user_id": user_id}) is not None


async def get_auth_users(chat_id: int) -> list:
    """Return list of user IDs authorized in a specific chat."""
    cursor = auth_col.find({"chat_id": chat_id})
    return [doc["user_id"] async for doc in cursor]


async def remove_auth_user(chat_id: int, user_id: int) -> bool:
    """Remove a user from a chat's authorized list."""
    result = await auth_col.delete_one({"chat_id": chat_id, "user_id": user_id})
    return result.deleted_count > 0
