from pytube import YouTube
from pyrogram import Client, filters
from dotenv import load_dotenv
import os


load_dotenv()
bot = Client(
    name=os.getenv('NAME'),
    api_id=os.getenv('API_ID'),
    api_hash=os.getenv('API_HASH'),
    bot_token=os.getenv('BOT_TOKEN')
)

@bot.on_message(filters.private)
def handle_message(client, message):
    bot.send_message(chat_id=message.chat.id, text="Welcome! to ytdownloadertgbot.")



bot.run()