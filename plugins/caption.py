from pyrogram import Client, filters 
from helper.database import db
from config import ADMINS 

@Client.on_message(filters.private & filters.command('set_caption') & filters.user(ADMINS))
async def add_caption(client, message):
    if len(message.command) == 1:
       return await message.reply_text("**__πΆπππ ππ π πππππππ ππ πππ.__\n\nπ΄π‘πππππ:- `/set_caption {filename}\n\nπΎ Size: {filesize}\n\nβ° Duration: {duration}`**")
    caption = message.text.split(" ", 1)[1]
    await db.set_caption(message.from_user.id, caption=caption)
    await message.reply_text("**β Your Caption Saved!")

    
@Client.on_message(filters.private & filters.command('del_caption') & filters.user(ADMINS))
async def delete_caption(client, message):
    caption = await db.get_caption(message.from_user.id)  
    if not caption:
       return await message.reply_text("__**π ππΎπ π³πΎπ½π π·π°ππ΄ π°π½π π²π°πΏππΈπΎπ½**__")
    await db.set_caption(message.from_user.id, caption=None)
    await message.reply_text("**βοΈ Your Caption Deleted!")
                                       
@Client.on_message(filters.private & filters.command('see_caption') & filters.user(ADMINS))
async def see_caption(client, message):
    caption = await db.get_caption(message.from_user.id)  
    if caption:
       await message.reply_text(f"**Your Caption :-**\n\n`{caption}`")
    else:
       await message.reply_text("No Caption")
