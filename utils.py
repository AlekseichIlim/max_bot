import os
from dotenv import load_dotenv
from maxapi import Bot, Dispatcher
import logging
file_path_report = 'D:/Sputnik_Bot_files/УЛ Спутник.xlsx'
file_path_month = 'D:/Sputnik_Bot_files/Итоги.xlsx'

ADMINS = [1892638646, ]
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
BOT_TOKEN = os.getenv("BOT_TOKEN_MAX")
GROUP_CHAT_ID = os.getenv("GROUP_CHAT_ID")

bot = Bot(token=BOT_TOKEN)


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)