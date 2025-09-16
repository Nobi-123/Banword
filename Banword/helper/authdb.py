# helper/authdb.py
#
# Database functions for managing authorized users per group.
# Each chat (group) has its own authorized users list.

from Banword.helper.database import db

# Collection for storing authorized users per group
auth_collection = db.auth_users  # Mongo collection: auth_users


async def add_auth_user(chat_id: int, user_id: int) -> bool:
    """
    Add a user to the authorized list of a specific chat.
    Returns True if added, False if already exists.
    """
    existing = await auth_collection.find_one({"chat_id": chat_id, "user_id": user_id})
    if not existing:
        await auth_collection.insert_one({"chat_id": chat_id, "user_id": user_id})
        return True
    return False


async def is_auth_user(chat_id: int, user_id: int) -> bool:
    """
    Check if a user is authorized in a given chat.
    Returns True if authorized, False otherwise.
    """
    return await auth_collection.find_one({"chat_id": chat_id, "user_id": user_id}) is not None


async def get_auth_users(chat_id: int) -> list:
    """
    Return a list of user IDs authorized in a specific chat.
    """
    cursor = auth_collection.find({"chat_id": chat_id})
    return [doc["user_id"] async for doc in cursor]


async def remove_auth_user(chat_id: int, user_id: int) -> bool:
    """
    Remove a user from a chat's authorized list.
    Returns True if deleted, False if user was not in the list.
    """
    result = await auth_collection.delete_one({"chat_id": chat_id, "user_id": user_id})
    return result.deleted_count > 0
