# 기술 설계서: yt-dlp 기반 VLC 스트리밍 MCP 서버

## 아키텍처 개요

```
Claude Desktop -> MCP Server (Python) -> Git Bash Process -> yt-dlp/VLC
```

## 기술 스택

- **언어**: Python 3.8+
- **MCP 프레임워크**: `mcp` 패키지
- **프로세스 관리**: `subprocess.Popen`
- **JSON 처리**: `json` (내장 모듈)
- **외부 도구**: `yt-dlp`, `VLC`, Git Bash

## 핵심 컴포넌트

### 1. MCP 서버 (main.py)

```python
# 주요 도구 정의
tools = [
    "stream_youtube",    # YouTube 스트리밍 실행
    "search_youtube"     # YouTube 영상 검색
]
```

### 2. 스트리밍 모듈 (streaming.py)

**기능**: YouTube URL을 VLC로 스트리밍

**구현**:
```python
def stream_youtube_video(url: str) -> dict:
    command = f'yt-dlp -o - "{url}" | vlc -'
    process = subprocess.Popen(
        command,
        shell=True,
        executable="C:/Program Files/Git/bin/bash.exe"
    )
    return {"status": "streaming", "pid": process.pid}
```

**입력**: YouTube URL (전체 URL)
**출력**: 프로세스 상태 및 PID

### 3. 검색 모듈 (search.py)

**기능**: YouTube 영상 검색

**구현**:
```python
def search_youtube_videos(query: str) -> list:
    command = f'yt-dlp "ytsearch10:{query}" --dump-json'
    result = subprocess.run(command, capture_output=True, text=True)
    videos = []
    for line in result.stdout.strip().split('\n'):
        data = json.loads(line)
        videos.append({
            "title": data["title"],
            "url": data["webpage_url"]
        })
    return videos
```

**입력**: 검색어 문자열
**출력**: 영상 제목과 URL 리스트

## 파일 구조

```
yt2vlc-mcp/
├── src/
│   ├── main.py          # MCP 서버 진입점
│   ├── streaming.py     # 스트리밍 기능
│   └── search.py        # 검색 기능
├── docs/
│   ├── PRD.md
│   └── TECHNICAL_DESIGN.md
├── requirements.txt
└── README.md
```

## 에러 처리

- **yt-dlp 실행 실패**: 명령어 오류 또는 URL 무효
- **VLC 실행 실패**: VLC 설치 확인 필요
- **Git Bash 경로 오류**: 경로 검증 및 fallback

## 보안 고려사항

- URL 입력 검증 (YouTube 도메인 확인)
- 명령어 인젝션 방지 (URL 이스케이핑)
- 프로세스 리소스 관리

## 성능 최적화

- 비동기 프로세스 실행
- 검색 결과 캐싱 (선택사항)
- 메모리 효율적인 스트리밍