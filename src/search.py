import subprocess
import json
import re


def search_youtube_videos(query: str) -> list:
    sanitized_query = sanitize_query(query)

    command = f'yt-dlp "ytsearch10:{sanitized_query}" --dump-json'

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            shell=True,
            executable="C:/Program Files/Git/bin/bash.exe"
        )

        if result.returncode != 0:
            raise Exception(f"yt-dlp 실행 실패: {result.stderr}")

        videos = []
        for line in result.stdout.strip().split('\n'):
            if line.strip():
                try:
                    data = json.loads(line)
                    videos.append({
                        "title": data.get("title", "제목 없음"),
                        "url": data.get("webpage_url", "")
                    })
                except json.JSONDecodeError:
                    continue

        return videos

    except Exception as e:
        raise Exception(f"YouTube 검색 실행 실패: {str(e)}")


def sanitize_query(query: str) -> str:
    if not query or not query.strip():
        raise ValueError("검색어가 비어있습니다")

    sanitized = re.sub(r'[^\w\s가-힣ㄱ-ㅎㅏ-ㅣ-]', '', query.strip())

    if not sanitized:
        raise ValueError("유효한 검색어가 없습니다")

    return sanitized