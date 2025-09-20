#!/usr/bin/env python3
import subprocess
import json
import re
import urllib.parse
from fastmcp import FastMCP

mcp = FastMCP("yt2vlc-mcp")


def sanitize_url(url: str) -> str:
    """YouTube URL 검증 및 정제"""
    if not url:
        raise ValueError("URL이 비어있습니다")

    youtube_pattern = r'^https?://(www\.)?(youtube\.com/watch\?v=|youtu\.be/)([a-zA-Z0-9_-]+)'
    if not re.match(youtube_pattern, url):
        raise ValueError("유효하지 않은 YouTube URL입니다")

    parsed = urllib.parse.urlparse(url)
    return urllib.parse.urlunparse(parsed)


def sanitize_query(query: str) -> str:
    """검색어 정제"""
    if not query or not query.strip():
        raise ValueError("검색어가 비어있습니다")

    sanitized = re.sub(r'[^\w\s가-힣ㄱ-ㅎㅏ-ㅣ-]', '', query.strip())
    if not sanitized:
        raise ValueError("유효한 검색어가 없습니다")

    return sanitized


@mcp.tool
def stream_youtube(url: str) -> str:
    """YouTube 영상을 VLC 플레이어로 스트리밍합니다"""
    try:
        sanitized_url = sanitize_url(url)
        command = f'yt-dlp -o - "{sanitized_url}" | vlc -'

        process = subprocess.Popen(
            ['C:/Program Files/Git/bin/bash.exe', '-c', command]
        )

        return f"스트리밍 시작됨 - PID: {process.pid}, URL: {sanitized_url}"

    except Exception as e:
        return f"스트리밍 실행 실패: {str(e)}"


@mcp.tool
def search_youtube(query: str) -> str:
    """YouTube에서 영상을 검색합니다"""
    try:
        sanitized_query = sanitize_query(query)
        command = f'yt-dlp "ytsearch5:{sanitized_query}" --flat-playlist --dump-single-json'

        process = subprocess.Popen(
            ['C:/Program Files/Git/bin/bash.exe', '-c', command],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        stdout, stderr = process.communicate()

        if process.returncode != 0:
            return f"yt-dlp 실행 실패: {stderr}"

        try:
            data = json.loads(stdout.strip())
            entries = data.get("entries", [])
            
            if not entries:
                return "검색 결과가 없습니다."
            
            result_text = "검색 결과:\n\n"
            for i, entry in enumerate(entries, 1):
                title = entry.get("title", "제목 없음")
                video_id = entry.get("id", "")
                url = f"https://www.youtube.com/watch?v={video_id}" if video_id else ""
                result_text += f"{i}. {title}\n   URL: {url}\n\n"
                
        except json.JSONDecodeError:
            return "검색 결과 파싱 실패"

        return result_text

    except Exception as e:
        return f"YouTube 검색 실행 실패: {str(e)}"


if __name__ == "__main__":
    mcp.run(transport="http", host="127.0.0.1", port=8000)