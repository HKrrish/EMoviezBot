from pyrogram import Client, filters 
from helper.database import db
from config import ADMINS 

@Client.on_message(filters.private & filters.command('set_caption') & filters.user(ADMINS))
async def add_caption(client, message):
    if len(message.command) == 1:
       return await message.reply_text("**__𝙶𝚒𝚟𝚎 𝚖𝚎 𝚊 𝚌𝚊𝚙𝚝𝚒𝚘𝚗 𝚝𝚘 𝚜𝚎𝚝.__\n\n𝙴𝚡𝚊𝚖𝚙𝚕𝚎:- `/set_caption {filename}\n\n💾 Size: {filesize}\n\n⏰ Duration: {duration}`**")
    caption = message.text.split(" ", 1)[1]
    await db.set_caption(message.from_user.id, caption=caption)
    await message.reply_text("**✅ Your Caption Saved!")

    
@Client.on_message(filters.private & filters.command('del_caption') & filters.user(ADMINS))
async def delete_caption(client, message):
    caption = await db.get_caption(message.from_user.id)  
    if not caption:
       return await message.reply_text("__**😔 𝚈𝙾𝚄 𝙳𝙾𝙽𝚃 𝙷𝙰𝚅𝙴 𝙰𝙽𝚈 𝙲𝙰𝙿𝚃𝙸𝙾𝙽**__")
    await db.set_caption(message.from_user.id, caption=None)
    await message.reply_text("**❌️ Your Caption Deleted!")
                                       
@Client.on_message(filters.private & filters.command('see_caption') & filters.user(ADMINS))
async def see_caption(client, message):
    caption = await db.get_caption(message.from_user.id)  
    if caption:
       await message.reply_text(f"**Your Caption :-**\n\n`{caption}`")
    else:
       await message.reply_text("No Caption")
