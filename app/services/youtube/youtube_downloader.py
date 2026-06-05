import os
import uuid

import yt_dlp


DOWNLOAD_DIR = "downloads"

os.makedirs(
    DOWNLOAD_DIR,
    exist_ok=True
)


def download_youtube_audio(url: str):

    file_id = str(uuid.uuid4())

    output_template = os.path.join(
        DOWNLOAD_DIR,
        file_id
    )

    ydl_opts = {
        "format": "bestaudio/best",

        "outtmpl": output_template + ".%(ext)s",

        "ffmpeg_location":
            r"C:\ffmpeg-2026-06-01-git-bf608f16fd-essentials_build\bin",

        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192"
            }
        ],

        "quiet": False,
        "noplaylist": True
    }

    with yt_dlp.YoutubeDL(
        ydl_opts
    ) as ydl:

        info = ydl.extract_info(
            url,
            download=True
        )

        title = info.get(
            "title",
            "YouTube Video"
        )

    final_audio_path = os.path.join(
        DOWNLOAD_DIR,
        f"{file_id}.mp3"
    )

    return final_audio_path, title