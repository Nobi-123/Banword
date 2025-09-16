# modules/auth.py
#
# Commands for managing authorized users in groups.
# Only group admins can use these commands.

from pyrogram import filters
from Banword import app
from Banword.helper.authdb import add_auth_user, remove_auth_user, get_auth_users

# -----------------------------
# /auth → authorize a user
# -----------------------------
@app.on_message(filters.command("auth") & filters.group & filters.admins)
async def authorize_user(client, message):
    user_id = None

    # Case 1: reply to user
    if message.reply_to_message and message.reply_to_message.from_user:
        user_id = message.reply_to_message.from_user.id

    # Case 2: argument (user_id or @username)
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


# -----------------------------
# /unauth → remove an authorized user
# -----------------------------
@app.on_message(filters.command("unauth") & filters.group & filters.admins)
async def unauthorize_user(client, message):
    user_id = None

    # Case 1: reply to user
    if message.reply_to_message and message.reply_to_message.from_user:
        user_id = message.reply_to_message.from_user.id

    # Case 2: argument (user_id or @username)
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

    if await remove_auth_user(message.chat.id, user_id):
        await message.reply_text(f"🗑️ Removed `{user_id}` from authorized users in this group")
    else:
        await message.reply_text(f"⚠️ User `{user_id}` is not authorized in this group.")


# -----------------------------
# /authusers → list all authorized users
# -----------------------------
@app.on_message(filters.command("authusers") & filters.group & filters.admins)
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
