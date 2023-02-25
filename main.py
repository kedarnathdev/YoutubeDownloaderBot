from pytube import YouTube
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton as IKB, InlineKeyboardMarkup as IKM
from dotenv import load_dotenv
import yt_dlp
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

def progress_callback(stream, chunk, bytes_remaining):
    size = video.filesize
    progress = int(((size - bytes_remaining) / size) * 100)
    print(progress)
    if progress%15==0:
        try:
            bot.edit_message_text(chat_id=msg.chat.id, message_id=msg.id, text=f"Downloading {progress} %")
        except:
            pass
def complete_callback(stream, file_handle):
    bot.edit_message_text(chat_id=msg.chat.id, message_id=msg.id, text="downloading finished")
def progress(current, total):
    progress = int(current*100/total)
    print(progress)
    if progress%25==0:
        try:
            bot.edit_message_text(chat_id=msg.chat.id, message_id=msg.id, text=f"Uploading to telegram {progress} %")
        except:
            pass



@bot.on_message(filters.command(['start']))
def handle_message(client, message):
    bot.send_message(chat_id=message.chat.id, text="Welcome! to ytdownloadertgbot.")
    
@bot.on_message(filters.command(['delete']))
def handle_delete(client, message):
    for i in os.listdir():
        if i.endswith('.py') or i.endswith('.txt') or i == "Dockerfile":
            pass
        else:
            os.remove(i)
            bot.send_message(chat_id=message.chat.id, text=f"Successfully deleted {i}")

@bot.on_message(filters.private)
def handle_urls(client, message):
    global url
    url = message
    bot.send_message(chat_id=message.chat.id, text="Select: ", reply_markup=keyboardAV)

@bot.on_callback_query()
def handle_callback(client, callbackData):
    if callbackData.data == "video":
        fetchVideoQualities(message=url)
    elif callbackData.data == "audio":
        fetchAudioQualities(message=url)
    else:
        yt = YouTube(url.text)
        yt.register_on_progress_callback(progress_callback)
        yt.register_on_complete_callback(complete_callback)
        global video
        y = yt.streams.get_by_itag(int(callbackData.data))
        video = y
        global msg
        msg = bot.send_message(chat_id=url.chat.id, text="Starting download..")
        if y.mime_type == 'video/mp4':
            wget.download(yt.thumbnail_url, out="thumb.jpg")
            y.download(output_path=os.getcwd(), filename="video.mp4")
            bot.send_video(chat_id=url.chat.id, video=open("video.mp4", "rb"), thumb="thumb.jpg", duration=yt.length, file_name=y.default_filename, supports_streaming=True, progress=progress)
            os.remove("video.mp4")
            os.remove("thumb.jpg")
        else:
            wget.download(yt.thumbnail_url, out="thumb.jpg")
            y.download(output_path=os.getcwd(), filename="music.mp3")
            bot.send_audio(chat_id=url.chat.id, audio=open("music.mp3", "rb"), file_name=y.default_filename[:len(y.default_filename)-3]+'.mp3', duration=yt.length, title=y.default_filename[:len(y.default_filename)-3], thumb="thumb.jpg", progress=progress, performer=yt.author)
            os.remove("music.mp3")
            os.remove("thumb.jpg")


bot.run()
