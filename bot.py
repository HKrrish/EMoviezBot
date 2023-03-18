from pyrogram import Client, idle
from config import API_ID, API_HASH, BOT_TOKEN, BOT_TOKEN2, FORCE_SUB, PORT
from aiohttp import web
from route import web_server

if __name__ == "__main__" :
    plugins = dict(root="plugins")
    app1 = Client(
        "Client1",
        bot_token=BOT_TOKEN1,
        api_id=API_ID,
        api_hash=API_HASH,
        plugins=plugins
    )
    app2 = Client( # This is 2nd client. add much as you wish. but remember to edit starting process
        "Client2",
        bot_token=BOT_TOKEN2,
        api_id=API_ID,
        api_hash=API_HASH,
        plugins=plugins
    )
    app = web.AppRunner(web_server())
    await app.setup()
    bind_address = "0.0.0.0"       
    await web.TCPSite(app, bind_address, PORT).start()     
    print(f"Started ⚡️")
      

    print("Waking Up Client 1")
    app1.start() # Starting Client 1
    print("Waking Up Client 2")
    app2.start() # Starting Client 2
    print("Everything Ok! Enjoy Multi Client! Lol!") # Remove this shit if you like lmao
    idle()
