from pyrogram import filters
from pyrogram.types import Message
from Banword import app
from config import OWNER_ID
from Banword.helper.authdb import add_auth_user, remove_auth_user, get_auth_users

# -------------------
# Custom admin filter
# -------------------
def admin_only():
    async def filter_func(_, __, message: Message):
        if not message.from_user:
            return False
        member = await message.chat.get_member(message.from_user.id)
        return member.status in ("administrator", "creator")
    return filters.create(filter_func)

# -------------------
# /auth command
# -------------------
@app.on_message(filters.command("auth") & filters.group & admin_only())
async def auth_cmd(client, message: Message):
    # Determine the target user
    user_id = None
    if message.reply_to_message and message.reply_to_message.from_user:
        user_id = message.reply_to_message.from_user.id
    elif message.entities:
        for ent in message.entities:
            if ent.type == "text_mention":
                user_id = ent.user.id
                break

    if not user_id:
        await message.reply("⚠️ Reply to a user's message or mention the user to authorize them.")
        return

    # Add the user to authorized list
    await add_auth_user(message.chat.id, user_id)
    await message.reply(f"✅ User `{user_id}` is now authorized in this group.")

# -------------------
# /unauth command
# -------------------
@app.on_message(filters.command("unauth") & filters.group & admin_only())
async def unauth_cmd(client, message: Message):
    # Determine the target user
    user_id = None
    if message.reply_to_message and message.reply_to_message.from_user:
        user_id = message.reply_to_message.from_user.id
    elif message.entities:
        for ent in message.entities:
            if ent.type == "text_mention":
                user_id = ent.user.id
                break

    if not user_id:
        await message.reply("⚠️ Reply to a user's message or mention the user to remove authorization.")
        return

    # Prevent removal of owner
    if user_id == OWNER_ID:
        await message.reply("⚠️ You cannot remove the bot owner from authorized users.")
        return

    await remove_auth_user(message.chat.id, user_id)
    await message.reply(f"❌ User `{user_id}` is no longer authorized in this group.")

# -------------------
# /authusers command
# -------------------
@app.on_message(filters.command("authusers") & filters.group & admin_only())
async def authusers_cmd(client, message: Message):
    auth_list = await get_auth_users(message.chat.id)
    if not auth_list:
        await message.reply("⚠️ No authorized users in this group yet.")
        return

    text = "✅ Authorized Users:\n\n" + "\n".join([f"- `{uid}`" for uid in auth_list])
    await message.reply(text)

# -------------------
# Ensure bot owner is always authorized
# -------------------
@app.on_message(filters.group)
async def ensure_owner_authorized(_, message: Message):
    chat_id = message.chat.id
    owner_auth_list = await get_auth_users(chat_id)
    if OWNER_ID not in owner_auth_list:
        await add_auth_user(chat_id, OWNER_ID)
