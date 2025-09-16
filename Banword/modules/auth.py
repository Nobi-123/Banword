from pyrogram import filters
from Banword import app
from config import OWNER_ID
from helper.auth import add_authorized_user
from helper.auth import get_authorized_users

@app.on_message(filters.command("auth") & filters.user(OWNER_ID))
async def authorize_user(client, message):
    user_id = None

    # Case 1: reply to a user's message
    if message.reply_to_message and message.reply_to_message.from_user:
        user_id = message.reply_to_message.from_user.id

    # Case 2: pass a username or ID in the command
    elif len(message.command) > 1:
        arg = message.command[1]

        # If it's numeric, assume user ID
        if arg.isdigit():
            user_id = int(arg)
        # If it's username, try to resolve
        else:
            try:
                user = await client.get_users(arg)
                user_id = user.id
            except Exception:
                await message.reply_text("⚠️ Invalid username or ID.")
                return

    # If still no user found
    if not user_id:
        await message.reply_text("⚠️ Reply to a user or provide their @username/userid.")
        return

    # Add user to auth list
    if add_authorized_user(user_id):
        await message.reply_text(f"✅ Authorized user `{user_id}`")
    else:
        await message.reply_text(f"⚠️ User `{user_id}` is already authorized.")

@app.on_message(filters.command("authusers") & filters.user(OWNER_ID))
async def list_authorized_users(client, message):
    users = get_authorized_users()

    if not users:
        await message.reply_text("⚠️ No authorized users yet.")
        return

    text = "**Authorized Users:**\n\n"
    for uid in users:
        try:
            user = await client.get_users(uid)
            name = f"{user.first_name or ''} {user.last_name or ''}".strip()
            mention = user.mention if user else str(uid)
            text += f"• {mention} (`{uid}`)\n"
        except Exception:
            text += f"• `{uid}` (not found)\n"

    await message.reply_text(text)
