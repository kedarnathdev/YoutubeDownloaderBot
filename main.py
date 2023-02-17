from pytube import YouTube
from pyrogram import Client, filters
import os

bot = Client(
    name=os.environ.get('NAME'),
    api_id=os.environ.get('API_ID'),
    api_hash=os.environ.get('API_HASH'),
    bot_token=os.environ.get('BOT_TOKEN')
)

bot.on_message(filters.command(['start']))
def start(client, message):
    bot.send_message(chat_id=message.chat.id, text="Welcome! to ytdownloadertgbot.")
