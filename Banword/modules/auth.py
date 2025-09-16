# modules/auth.py

from pyrogram import filters
from Banword import app
from config import OWNER_ID
from helper.authdb import add_auth_user, is_authorized, get_auth_users

@app.on_message(filters.command("auth") & filters.user(OWNER_ID))
async def authorize_user(client, message):
    user_id = None

    # Case 1: reply
    if message.reply_to_message and message.reply_to_message.from_user:
        user_id = message.reply_to_message.from_user.id

    # Case 2: argument
    elif len(message.command) > 1:
        arg = message.command[1]
        if arg.isdigit():
            user_id = int(arg)
        else:
            try:
                user = await client.get_users(arg)
                user_id = user.id
            except Exception:
                await message.reply_text("⚠️ Invalid username or ID.")
                return

    if not user_id:
        await message.reply_text("⚠️ Reply to a user or provide @username/userid.")
        return

    if await add_auth_user(message.chat.id, user_id):
        await message.reply_text(f"✅ Authorized user `{user_id}` in this group")
    else:
        await message.reply_text(f"⚠️ User `{user_id}` is already authorized here.")
        

@app.on_message(filters.command("authusers") & filters.group)
async def list_auth_users(client, message):
    users = await get_auth_users(message.chat.id)

    if not users:
        await message.reply_text("⚠️ No authorized users in this group.")
        return

    text = "👑 **Authorized Users in this Group:**\n\n"
    for uid in users:
        try:
            user = await client.get_users(uid)
            mention = user.mention if user else f"`{uid}`"
            text += f"• {mention} (`{uid}`)\n"
        except Exception:
            text += f"• `{uid}` (not found)\n"

    await message.reply_text(text)
