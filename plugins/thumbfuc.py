from pyrogram import Client, filters
from helper.database import db
from config import ADMINS 

@Client.on_message(filters.private & filters.command(['viewthumb']) & filters.user(ADMINS))
async def viewthumb(client, message):    
    thumb = await db.get_thumbnail(message.from_user.id)
    if thumb:
       await client.send_photo(
	   chat_id=message.chat.id, 
	   photo=thumb)
    else:
        await message.reply_text("No Thumbnail Yet.") 
		
@Client.on_message(filters.private & filters.command(['delthumb']) & filters.user(ADMINS))
async def removethumb(client, message):
    await db.set_thumbnail(message.from_user.id, file_id=None)
    await message.reply_text("❌️ Your Thumbnail Deleted!")
	
@Client.on_message(filters.private & filters.photo & filters.user(ADMINS))
async def addthumbs(client, message):
    mkn = await message.reply_text("...")
    await db.set_thumbnail(message.from_user.id, file_id=message.photo.file_id)                
    await mkn.edit("✅️ Your Thumbnail Saved!")
