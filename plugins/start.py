from asyncio import sleep
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ForceReply, CallbackQuery
from pyrogram.errors import FloodWait
import humanize
import random
from helper.txt import mr
from helper.database import db
from config import START_PIC, FLOOD, ADMINS, LOG_CHANNEL 

LOG_TEXT_P = """#NewUser
ID - <code>{}</code>
Name - {}
"""

@Client.on_message(filters.private & filters.command(["start"]))
async def start(client, message):
    user = message.from_user
    if not await db.is_user_exist(user.id):
        await db.add_user(user.id) 
        await client.send_message(LOG_CHANNEL, text=LOG_TEXT_P.format(message.from_user.id, message.from_user.mention))            
    txt=f"**👋 Hai {user.mention},\nI'm Simple Movie Searcher Bot.** 🎥\n\nYou can use me to search any movie. Just press below Button and start searching."
    button=InlineKeyboardMarkup([[
        InlineKeyboardButton('Search Here', switch_inline_query_current_chat=''),
        InlineKeyboardButton('Go Inline', switch_inline_query='')
        ],[
        InlineKeyboardButton('DMCA', callback_data='dmca'),
        InlineKeyboardButton('Help', callback_data='help')
        ],[
        InlineKeyboardButton('Channel', url='https://t.me/The_Entertainment')
        ]])
    if START_PIC:
        await message.reply_photo(START_PIC, caption=txt, reply_markup=button)       
    else:
        await message.reply_text(text=txt, reply_markup=button, disable_web_page_preview=True)
   

@Client.on_message(filters.private & (filters.document | filters.audio | filters.video) & filters.user(ADMINS))
async def rename_start(client, message):
    file = getattr(message, message.media.value)
    filename = file.file_name
    filesize = humanize.naturalsize(file.file_size) 
    fileid = file.file_id
    try:
        text = f"""**What do you to do with this file?**\n\n**File Name** : `{filename}`\n\n**File Size** : `{filesize}`"""
        buttons = [[ InlineKeyboardButton("Start Rename", callback_data="rename") ],
                   [ InlineKeyboardButton("Cancel", callback_data="cancel") ]]
        await message.reply_text(text=text, reply_to_message_id=message.id, reply_markup=InlineKeyboardMarkup(buttons))
        await sleep(FLOOD)
    except FloodWait as e:
        await sleep(e.value)
        text = f"""**What do you to do with this file?**\n\n**File Name** : `{filename}`\n\n**File Size** : `{filesize}`"""
        buttons = [[ InlineKeyboardButton("Start Rename", callback_data="rename") ],
                   [ InlineKeyboardButton("Cancel", callback_data="cancel") ]]
        await message.reply_text(text=text, reply_to_message_id=message.id, reply_markup=InlineKeyboardMarkup(buttons))
    except:
        pass

@Client.on_callback_query()
async def cb_handler(client, query: CallbackQuery):
    data = query.data 
    if data == "start":
        await query.message.edit_text(
            text=f"""👋 Hai {query.from_user.mention} \nI'm Simple Movie Searcher Bot.** 🎥\n\nYou can use me to search any movie. Just press below Button and start searching.""",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton('Search Movie', switch_inline_query_current_chat=''),
                InlineKeyboardButton('Help', callback_data='help')
                ]]
                )
            )
    elif data == "help":
        await query.message.edit_text(
            text=mr.HELP_TXT,
            reply_markup=InlineKeyboardMarkup([[
               InlineKeyboardButton("Search Movie", switch_inline_query_current_chat=''),
               InlineKeyboardButton("Back", callback_data = "start")
               ]]
            )
        )
    elif data == "dmca":
        await query.message.edit_text(
            text=mr.DMCA_TXT.format(client.mention),
            disable_web_page_preview = True,
            reply_markup=InlineKeyboardMarkup([[
               InlineKeyboardButton("Close", callback_data = "close"),
               InlineKeyboardButton("Back", callback_data = "start")
               ]]
            )
        )
    elif data == "close":
        try:
            await query.message.delete()
            await query.message.reply_to_message.delete()
        except:
            await query.message.delete()
