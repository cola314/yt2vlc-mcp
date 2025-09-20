# yt2vlc-mcp

YouTube 영상을 yt-dlp와 VLC를 사용해 스트리밍하는 MCP 서버입니다.

## 기능

- **YouTube 스트리밍**: YouTube URL을 VLC 플레이어로 실시간 스트리밍
- **YouTube 검색**: yt-dlp를 사용한 YouTube 영상 검색

## 필요 도구

- Python 3.8+
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [VLC Media Player](https://www.videolan.org/vlc/)
- Git Bash (Windows)

## 설치

1. 의존성 설치:
```bash
pip install -r requirements.txt
```

2. 외부 도구 설치:
```bash
# yt-dlp 설치
pip install yt-dlp

# VLC 설치 (https://www.videolan.org/vlc/)
# Git Bash 설치 (https://git-scm.com/)
```

## MCP 서버 등록

### Claude Desktop에서 등록

1. Claude Desktop 설정 파일 열기:
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`

2. 설정 파일에 MCP 서버 추가:
```json
{
  "mcpServers": {
    "yt2vlc": {
      "command": "python",
      "args": ["/path/to/mcp/main.py"],
      "cwd": "/path/to/mcp/"
    }
  }
}
```

3. Claude Desktop 재시작

### 경로 설정

- `command`: Python 실행 파일 경로
- `args`: main.py의 절대 경로
- `cwd`: 프로젝트 루트 디렉토리

## 사용법

Claude Desktop에서 다음과 같이 사용할 수 있습니다:

### YouTube 스트리밍
```
YouTube 영상을 스트리밍해줘: https://www.youtube.com/watch?v=VIDEO_ID
```

### YouTube 검색
```
"파이썬 튜토리얼" 영상을 검색해줘
```

## 도구 설명

### stream_youtube
- **입력**: YouTube URL
- **출력**: VLC에서 스트리밍 시작, 프로세스 정보 반환

### search_youtube
- **입력**: 검색 키워드
- **출력**: 상위 10개 검색 결과 (제목, URL)

## 보안

- YouTube URL 유효성 검증
- 명령어 인젝션 방지
- 사용자 입력 새니타이징

## 문제 해결

### Git Bash 경로 오류
Windows에서 Git Bash 경로가 다른 경우:
```python
# src/streaming.py, src/search.py 수정
executable="C:/Git/bin/bash.exe"  # 실제 설치 경로로 변경
```

### VLC 실행 실패
VLC가 PATH에 없는 경우, 전체 경로 사용:
```bash
yt-dlp -o - "URL" | "C:/Program Files/VideoLAN/VLC/vlc.exe" -
```