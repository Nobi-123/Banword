from pyrogram import filters
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from Banword import Banword as app

# Show Help Menu
@app.on_callback_query(filters.regex("^show_help$"))
async def show_help(_, query: CallbackQuery):
    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Aᴅᴍɪɴ Cᴏᴍᴍᴀɴᴅs", callback_data="help_admin")],
            [InlineKeyboardButton("Oᴛʜᴇʀ Cᴏᴍᴍᴀɴᴅs", callback_data="help_misc")],
            [InlineKeyboardButton("« Bᴀᴄᴋ", callback_data="back_to_start")]
        ]
    )
    await query.message.edit_text(
        "**Hᴇʟᴘ Mᴇɴᴜ**\nSᴇʟᴇᴄᴛ ᴀ ᴄᴀᴛᴇɢᴏʀʏ ʙᴇʟᴏᴡ:",
        reply_markup=keyboard
    )

# Admin Commands
@app.on_callback_query(filters.regex("^help_admin$"))
async def help_admin(_, query: CallbackQuery):
    await query.message.edit_text(
        """**Admin Commands:**
•owner = @aashikteam""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("« Bᴀᴄᴋ", callback_data="show_help")]]
        )
    )


# Misc Commands
@app.on_callback_query(filters.regex("^help_misc$"))
async def help_misc(_, query: CallbackQuery):
    await query.message.edit_text(
        """**Other Commands:**
• /start - Start the bot
• /stats - Bot's statistics
• /ping - Bot's Pinging
• /addsudo - Add sudo user
• /delsudo - Remove sudo""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("« Bᴀᴄᴋ", callback_data="show_help")]]
        )
    )
