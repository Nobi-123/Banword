import re
import asyncio
from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from Banword import app
from config import OTHER_LOGS, BOT_USERNAME
from Banword.helper.authdb import get_auth_users

# -------------------
# Banned words list
# -------------------
BAD_WORDS = [
    # 18+ words
    "18+", "sex", "porn", "nude", "blowjob", "boobs", "bobs", "condom", "xxx", "adult", "nangi", "randi", 
    # Common offensive words
    "chutiya", "madarchod", "bhenchod", "gaand", "gand", "lund", "ch**d", "g***i", "harami", "kutte", "kutta",
    "gandu", "madharchod", "lundoo", "lodu", "bhains", "chod", "randi", "randa", "haramzada", "randi ka bacha",
    "bhosdiwala", "bhosdike", "mc", "mcchod", "randi ki aulaad", "gand mara", "lund mar", "lauda", "loda",
    "chodu", "chut", "chutiyapa", "chutiye", "chut ke", "chut ke laude", "chut ke bache", "bhosadike", "bsdk",
    "allen", "oswaal", "t.me/", "https://t.me/", "www", "bkl",
    # Slang variations with stars
    "ch**d", "g***i", "m**ch*d", "b**chod", "b***chod"
]

BAD_PATTERN = re.compile(r"|".join([re.escape(word) for word in BAD_WORDS]), re.IGNORECASE)

# -------------------
# Message filter
# -------------------
@app.on_message(filters.group & filters.text & ~filters.via_bot)
async def filter_18(client, message: Message):
    text = message.text or ""
    if not BAD_PATTERN.search(text):
        return

    user = message.from_user
    if not user:
        return

    # Check if user is authorized in this group
    auth_users = await get_auth_users(message.chat.id)
    if user.id in auth_users:
        return  # skip deletion

    # Delete the message
    try:
        await message.delete()
    except:
        return

    # Send warning in group
    mention = f"[{user.first_name}](tg://user?id={user.id})"
    warn_text = f"{mention}, Abusive messages are not allowed!"
    cancel_btn = InlineKeyboardMarkup([[InlineKeyboardButton("Cancel", callback_data="close")]])

    try:
        warn = await message.reply(warn_text, reply_markup=cancel_btn)
        await asyncio.sleep(10)
        await warn.delete()
    except:
        pass

    # Logging to OTHER_LOGS
    username = f"@{user.username}" if user.username else "No username"
    group_name = message.chat.title
    chat_id = message.chat.id

    log_text = f"""
🚫 **18+ or Abusive Message Deleted**

**👤 User:** {mention}
**🆔 User ID:** `{user.id}`
**🔗 Username:** {username}
**🏷️ Group:** `{group_name}`
**🆔 Chat ID:** `{chat_id}`
**💬 Message:** `{text}`

🤖 **Bot:** @{BOT_USERNAME}
"""

    try:
        await client.send_message(
            OTHER_LOGS,
            log_text,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("➕ Add to Your Group", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")]
            ])
        )
    except Exception as e:
        print(f"[LOG SEND ERROR] {e}")

# -------------------
# Cancel button handler
# -------------------
@app.on_callback_query(filters.regex("close"))
async def close_btn(client, callback_query):
    try:
        await callback_query.message.delete()
    except:
        pass
