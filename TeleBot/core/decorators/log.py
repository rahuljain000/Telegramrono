from functools import wraps
import datetime
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram import errors
from TeleBot.mongo.log_channel_db import get_log_channel,unset_log


def loggable(func):
        @wraps(func)
        async def log(client,update, lang):
            result = await func(client, update, lang)
            message =  update.message if isinstance(update,CallbackQuery) else update
            chat = message.chat
            if result:
                result += f"\n\n**ᴇᴠᴇɴᴛ ꜱᴛᴀᴍᴘ** : {datetime.datetime.utcnow().strftime('%H:%M - %d-%m-%Y')}"
                btn = InlineKeyboardMarkup([[InlineKeyboardButton("• ʟɪɴᴋ •",url = message.link)]])
                channel = await get_log_channel(chat.id)
                if channel:
                    try:
                        await client.send_message(channel,result,reply_markup = btn)
                    except errors.BadRequest as e:
                         await client.send_message(chat.id,f"**ᴀɴ ᴇʀʀᴏʀ ᴏᴄᴄᴜʀɴɪɴɢ ᴡʜɪʟᴇ ʟᴏɢɢɪɴɢ:**\n{e.MESSAGE}\n\n**ᴜɴꜱᴇᴛᴛɪɴɢ ʟᴏɢ ᴄʜᴀɴɴᴇʟ...**")
                         await unset_log(chat.id)        
            return result
        return log