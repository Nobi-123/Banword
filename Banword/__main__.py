import asyncio
import importlib
from pyrogram import idle
from Banword import app  # fixed import
from Banword.modules import ALL_MODULES
from config import LOGGER_ID, BOT_USERNAME

loop = asyncio.get_event_loop()

async def roy_bot():
    # Import all modules dynamically
    for all_module in ALL_MODULES:
        importlib.import_module(f"Banword.modules.{all_module}")

    print("• Bot Started Successfully.")
    await idle()
    print("• Don't edit baby, otherwise you get an error: @ProtectronLogs")

    # Send alive message
    await app.send_message(
        LOGGER_ID,
        "**✦ ɪ ᴀᴍ ᴀʟɪᴠᴇ ʙᴀʙʏ.\n\n✦ ᴊᴏɪɴ - @HamsterUpdatess**"
    )

if __name__ == "__main__":
    loop.run_until_complete(roy_bot())
