from pytube import YouTube
from pyrogram.types import InlineKeyboardButton as IKB, InlineKeyboardMarkup as IKM

url = "https://youtu.be/YpJYSIRa03Q"

yt = YouTube(url)
y = yt.streams.filter(only_audio=True)
for i in y:
    print(i.abr)