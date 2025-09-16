from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from Banword import app
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
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    elif message.entities:
        # Check if user mentioned
        user_id = None
        for ent in message.entities:
            if ent.type == "text_mention":
                user_id = ent.user.id
                break
    else:
        await message.reply("⚠️ Reply to a user's message or mention the user to authorize them.")
        return

    if not user_id:
        await message.reply("⚠️ Could not find the user.")
        return

    await add_auth_user(message.chat.id, user_id)
    await message.reply(f"✅ User `{user_id}` is now authorized in this group.")

# -------------------
# /unauth command
# -------------------
@app.on_message(filters.command("unauth") & filters.group & admin_only())
async def unauth_cmd(client, message: Message):
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    elif message.entities:
        user_id = None
        for ent in message.entities:
            if ent.type == "text_mention":
                user_id = ent.user.id
                break
    else:
        await message.reply("⚠️ Reply to a user's message or mention the user to remove authorization.")
        return

    if not user_id:
        await message.reply("⚠️ Could not find the user.")
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
