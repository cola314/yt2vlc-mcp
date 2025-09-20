#!/usr/bin/env python3
import subprocess
import json
import re
import urllib.parse

def sanitize_query(query: str) -> str:
    if not query or not query.strip():
        raise ValueError("검색어가 비어있습니다")

    sanitized = re.sub(r'[^\w\s가-힣ㄱ-ㅎㅏ-ㅣ-]', '', query.strip())

    if not sanitized:
        raise ValueError("유효한 검색어가 없습니다")

    return sanitized

def search_youtube_test(query: str) -> str:
    """YouTube에서 영상을 검색합니다 (테스트용)"""
    try:
        sanitized_query = sanitize_query(query)
        command = f'yt-dlp "ytsearch10:{sanitized_query}" --flat-playlist --dump-single-json'

        process = subprocess.Popen(
            ['C:/Program Files/Git/bin/bash.exe', '-c', command],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        stdout, stderr = process.communicate()

        if process.returncode != 0:
            return f"yt-dlp 실행 실패: {stderr}"

        videos = []
        for line in stdout.strip().split('\n'):
            if line.strip():
                try:
                    data = json.loads(line)
                    videos.append({
                        "title": data.get("title", "제목 없음"),
                        "url": data.get("webpage_url", "")
                    })
                except json.JSONDecodeError:
                    continue

        if not videos:
            return "검색 결과가 없습니다."

        result_text = "검색 결과:\n\n"
        for i, video in enumerate(videos, 1):
            result_text += f"{i}. {video['title']}\n   URL: {video['url']}\n\n"

        return result_text

    except Exception as e:
        return f"YouTube 검색 실행 실패: {str(e)}"

def test_search():
    print("=== YouTube 검색 테스트 ===")
    print("검색어: 쇼팽")
    print("")
    
    result = search_youtube_test("쇼팽")
    print(result)

if __name__ == "__main__":
    test_search()
