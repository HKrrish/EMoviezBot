import re, os
from os import environ 

id_pattern = re.compile(r'^.\d+$')

# temp db for banned 
class temp(object):
    BANNED_USERS = []
    BANNED_CHATS = []
    ME = None
    CURRENT=int(os.environ.get("SKIP", 2))
    CANCEL = False
    MELCOW = {}
    U_NAME = None
    B_NAME = None 

#Basic
API_ID = os.environ.get("API_ID", "")
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "") 

#jaroora nhi hai vese
FORCE_SUB = os.environ.get("FORCE_SUB", "") 

#for database 
DB_NAME = os.environ.get("DB_NAME","Entertainment")     
DB_URL = os.environ.get("DB_URL","")
COLLECTION_NAME = environ.get('COLLECTION_NAME', 'Telegram_files')

# Admins, Channels & Users
CHANNELS = [int(ch) if id_pattern.search(ch) else ch for ch in environ.get('CHANNELS', '-1001815834835').split()]
auth_users = [int(user) if id_pattern.search(user) else user for user in environ.get('AUTH_USERS', '').split()]
AUTH_USERS = (auth_users + ADMINS) if auth_users else []
auth_channel = environ.get('AUTH_CHANNEL')
auth_grp = environ.get('AUTH_GROUP')
AUTH_CHANNEL = int(auth_channel) if auth_channel and id_pattern.search(auth_channel) else None
AUTH_GROUPS = [int(ch) for ch in auth_grp.split()] if auth_grp else None
support_chat_id = environ.get('SUPPORT_CHAT_ID')

LOG_CHANNEL = "-1001361102488"
INDEX_REQ_CHANNEL = int(environ.get('INDEX_REQ_CHANNEL', LOG_CHANNEL))

CUSTOM_FILE_CAPTION = environ.get("CUSTOM_FILE_CAPTION")
USE_CAPTION_FILTER = bool(environ.get('USE_CAPTION_FILTER', False))
CACHE_TIME = int(environ.get('CACHE_TIME', 300))
FLOOD = int(os.environ.get("FLOOD", "10"))
MAX_BTN = int(environ.get('MAX_BTN', "7"))
START_PIC = os.environ.get("START_PIC", "")
ADMINS = [int(admin) if id_pattern.search(admin) else admin for admin in os.environ.get('ADMINS', '').split()]
PORT = os.environ.get('PORT', '8080')
