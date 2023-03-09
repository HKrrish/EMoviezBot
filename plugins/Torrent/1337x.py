#Dj
import os
import aiohttp
import json
from pyrogram import Client, filters, emoji, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

m = None
i = 0
a = None
query = None


@Client.on_message(filters.command(["torrent"]))
async def findtorr(_, message):
    global m
    global i
    global a
    global query
    try:
        await message.delete()
    except:
        pass
    if len(message.command) < 2:
        await message.reply_text("Use: /torrent `movie/series`")
        return
    query = message.text.split(None, 1)[1].replace(" ", "%20")
    m = await message.reply_text("Searching...")
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://api.api-zero.workers.dev/1337x/{query}") \
                    as resp:
                a = json.loads(await resp.text())
    except:
        await m.edit_text("Found Nothing.")
        return
    result = (
        f"**--Page-- - {i+1}**\n\n"
        f"🎬 **Name**: {a[i]['Name']}\n\n"
        f"• **Uploaded By**: {a[i]['UploadedBy']} "
        f"{a[i]['DateUploaded']}\n" 
        f"• **Type**: {a[i]['Type']} "
        f"• **Category**: {a[i]['Category']}\n"
        f"• **Language**: {a[i]['Language']}\n"
        f"• **Checked**: {a[i]['LastChecked']}\n"
        f"• **Seeders**: {a[i]['Seeders']} & "
        f"• **Leeches**: {a[i]['Leechers']}\n\n"
        f"🧲 **--Magnet--**: `{a[i]['Magnet']}`\n\n"
        f"~ (@EMoviezBot) ~"
    )
    await m.edit_text(
        result,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(f"Next",
                                         callback_data="next"),
                    InlineKeyboardButton(f"{emoji.CROSS_MARK}",
                                         callback_data="delete")
                ]
            ]
        ),
        parse_mode=enums.ParseMode.MARKDOWN,
    )


@Client.on_callback_query(filters.regex("next"))
async def callback_query_next(_, message):
    global i
    global m
    global a
    global query
    i += 1
    result = (
        f"**--Page-- - {i+1}**\n\n"
        f"🎬 **Name**: {a[i]['Name']}\n\n"
        f"• **Uploaded By**: {a[i]['UploadedBy']} "
        f"{a[i]['DateUploaded']}\n" 
        f"• **Type**: {a[i]['Type']} "
        f"• **Category**: {a[i]['Category']}\n"
        f"• **Language**: {a[i]['Language']}\n"
        f"• **Checked**: {a[i]['LastChecked']}\n"
        f"• **Seeders**: {a[i]['Seeders']} & "
        f"• **Leeches**: {a[i]['Leechers']}\n\n"
        f"🧲 **--Magnet--**: `{a[i]['Magnet']}`\n\n"
        f"~ (@EMoviezBot) ~"
    )
    await m.edit_text(
        result,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(f"Prev",
                                         callback_data="previous"),
                    InlineKeyboardButton(f"{emoji.CROSS_MARK}",
                                         callback_data="delete"),
                    InlineKeyboardButton(f"Next",
                                         callback_data="next")
                    
                ]
            ]
        ),
        parse_mode=enums.ParseMode.MARKDOWN,
    )


@Client.on_callback_query(filters.regex("previous"))
async def callback_query_previous(_, message):
    global i
    global m
    global a
    global query
    i -= 1
    result = (
        f"**--Page-- - {i+1}**\n\n"
        f"🎬 **Name**: {a[i]['Name']}\n\n"
        f"• **Uploaded By**: {a[i]['UploadedBy']} "
        f"{a[i]['DateUploaded']}\n" 
        f"• **Type**: {a[i]['Type']} "
        f"• **Category**: {a[i]['Category']}\n"
        f"• **Language**: {a[i]['Language']}\n"
        f"• **Checked**: {a[i]['LastChecked']}\n"
        f"• **Seeders**: {a[i]['Seeders']} & "
        f"• **Leeches**: {a[i]['Leechers']}\n\n"
        f"🧲 **--Magnet--**: `{a[i]['Magnet']}`\n\n"
        f"~ (@EMoviezBot) ~"
    )
    await m.edit_text(
        result,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(f"Prev",
                                         callback_data="previous"),
                    InlineKeyboardButton(f"{emoji.CROSS_MARK}",
                                         callback_data="delete"),
                    InlineKeyboardButton(f"Next",
                                         callback_data="next")
                ]
            ]
        ),
        parse_mode=enums.ParseMode.MARKDOWN,
    )


@Client.on_callback_query(filters.regex("delete"))
async def callback_query_delete(_, message):
    global m
    global i
    global a
    global query
    await m.delete()
    m = None
    i = 0
    a = None
    query = None
