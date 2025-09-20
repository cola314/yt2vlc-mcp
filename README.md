# yt2vlc-mcp

YouTube 영상을 VLC 플레이어로 스트리밍하는 MCP 서버

## 설치

```bash
pip install -r requirements.txt
```

## 실행

```bash
python main.py
```

서버는 `http://127.0.0.1:8000`에서 실행됩니다.

## MCP 클라이언트 연결

### Claude Desktop 연결 (프록시 사용)

Claude Desktop은 원격 MCP 서버를 직접 사용할 수 없으므로 프록시 서버를 사용합니다.

1. **MCP 서버 실행** (터미널 1):
```bash
python main.py
```

2. **프록시 서버 설정**: Claude Desktop 설정 파일 (`%APPDATA%\Claude\claude_desktop_config.json`)에 다음을 추가:

```json
{
  "mcpServers": {
    "yt2vlc-mcp": {
      "command": "python",
      "args": ["/path/to/proxy_server.py"],
    }
  }
}
```

**구조**: `Claude Desktop → STDIO → proxy_server.py → HTTP → main.py`

### Cursor 연결

Cursor의 MCP 설정 파일 (`.cursorrules` 또는 설정)에 다음을 추가하세요:

```json
{
  "mcp": {
    "servers": {
      "yt2vlc-mcp": {
        "url": "http://127.0.0.1:8000"
      }
    }
  }
}
```

## 사용 방법

### YouTube 검색
```
YouTube에서 "노래 제목" 검색해줘
```

### YouTube 스트리밍
```
https://www.youtube.com/watch?v=... 이 영상을 VLC로 재생해줘
```

## 필수 프로그램

- Python 3.7+
- VLC Media Player
- yt-dlp
- Git Bash