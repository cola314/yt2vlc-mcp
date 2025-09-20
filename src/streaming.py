import subprocess
import urllib.parse
import re


def stream_youtube_video(url: str) -> dict:
    sanitized_url = sanitize_url(url)

    command = f'yt-dlp -o - "{sanitized_url}" | vlc -'

    try:
        process = subprocess.Popen(
            command,
            shell=True,
            executable="C:/Program Files/Git/bin/bash.exe"
        )

        return {
            "status": "streaming",
            "pid": process.pid,
            "url": sanitized_url
        }
    except Exception as e:
        raise Exception(f"스트리밍 프로세스 시작 실패: {str(e)}")


def sanitize_url(url: str) -> str:
    if not url:
        raise ValueError("URL이 비어있습니다")

    youtube_pattern = r'^https?://(www\.)?(youtube\.com/watch\?v=|youtu\.be/)([a-zA-Z0-9_-]+)'

    if not re.match(youtube_pattern, url):
        raise ValueError("유효하지 않은 YouTube URL입니다")

    parsed = urllib.parse.urlparse(url)
    return urllib.parse.urlunparse(parsed)