from pytube import YouTube
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton as IKB, InlineKeyboardMarkup as IKM
from dotenv import load_dotenv
import os
import wget

keyboardAV = IKM([
    [IKB(text="Video 📽️", callback_data="video")],
    [IKB(text="Audio 🔉", callback_data="audio")]
])

load_dotenv()
bot = Client(
    name=os.getenv('NAME'),
    api_id=os.getenv('API_ID'),
    api_hash=os.getenv('API_HASH'),
    bot_token=os.getenv('BOT_TOKEN')
)

def fetchVideoQualities(message):
    l = []
    keyboardYT = IKM(l)
    y = YouTube(message.text).streams.filter(mime_type='video/mp4', progressive=True)
    for i in y:
        l.append([IKB(text=f'{i.resolution} Video 📽️ {i.filesize_mb} MB', callback_data=str(i.itag))])
    bot.send_message(chat_id=message.chat.id, text='Available Qualities', reply_markup=keyboardYT)

def fetchAudioQualities(message):
    l = []
    keyboardYT = IKM(l)
    y = YouTube(message.text).streams.filter(only_audio=True)
    for i in y:
        l.append([IKB(text=f'{i.abr} Audio 🔉 {i.filesize_mb} MB', callback_data=str(i.itag))])
    bot.send_message(chat_id=message.chat.id, text='Available Qualities', reply_markup=keyboardYT)


@bot.on_message(filters.command(['start']))
def handle_message(client, message):
    bot.send_message(chat_id=message.chat.id, text="Welcome! to ytdownloadertgbot.")

@bot.on_message(filters.private)
def handle_urls(client, message):
    global msg
    msg = message
    bot.send_message(chat_id=message.chat.id, text="Select: ", reply_markup=keyboardAV)

@bot.on_callback_query()
def handle_callback(client, callbackData):
    if callbackData.data == "video":
        fetchVideoQualities(message=msg)
    elif callbackData.data == "audio":
        fetchAudioQualities(message=msg)
    else:
        yt = YouTube(msg.text)
        y = yt.streams.get_by_itag(int(callbackData.data))
        if y.mime_type == 'video/mp4':
            wget.download(yt.thumbnail_url, out="thumb.jpg")
            y.download(output_path=os.getcwd(), filename="video.mp4")
            bot.send_video(chat_id=msg.chat.id, video=open("video.mp4", "rb"), thumb="thumb.jpg", duration=yt.length, file_name=y.default_filename, supports_streaming=True)
            os.remove("video.mp4")
            os.remove("thumb.jpg")
        else:
            wget.download(yt.thumbnail_url, out="thumb.jpg")
            y.download(output_path=os.getcwd(), filename="music.mp3")
            bot.send_audio(chat_id=msg.chat.id, audio=open("music.mp3", "rb"), file_name=y.default_filename[:len(y.default_filename)-3]+'.mp3', duration=yt.length, thumb="thumb.jpg")
            os.remove("music.mp3")
            os.remove("thumb.jpg")


bot.run()