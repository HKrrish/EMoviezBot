from pyrogram import Client 
from config import API_ID, API_HASH, BOT_TOKEN, FORCE_SUB, PORT
from aiohttp import web
from route import web_server

class Bot(Client):

    def __init__(self):
        super().__init__(
            name="renamer",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            workers=200,
            plugins={"root": "plugins"},
            sleep_threshold=15,
        )

    async def start(self):
        await super().start()
        me = await self.get_me()
        self.mention = me.mention
        self.username = me.username 
    
        app = web.AppRunner(await web_server())
        await app.setup()
        bind_address = "0.0.0.0"       
        await web.TCPSite(app, bind_address, PORT).start()     
        print(f"{me.first_name} Started ⚡️")
      

    async def stop(self, *args):
        await super().stop()      
        print("Bot Stopped")
       

bot=Bot()
bot.run()
