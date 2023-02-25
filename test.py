import yt_dlp

y = {
    "format": "best",
    "outtmpl": "video.mp4"
}

ytd = yt_dlp.YoutubeDL(y)
url = "https://youtu.be/8s2DQBhEvoA"
result = ytd.extract_info(url)

print(round(result["filesize"]/1024/1024, 2))
print(round(result["filesize_approx"]/1024/1024, 2))
print(result["title"])
print(result["uploader"])
print(result["duration"])
