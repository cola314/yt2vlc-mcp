
# PRD: yt-dlp 기반 VLC 스트리밍 MCP 서버

## 개요

* 본 프로젝트는 **Python 기반 MCP 서버**로, Git Bash 프로세스를 통해 `yt-dlp`와 `VLC`를 연동하여 YouTube 영상을 스트리밍한다.
* 또한, `yt-dlp`의 검색 기능을 활용하여 YouTube 영상을 검색할 수 있다.

---

## 목표

1. **YouTube URL을 입력받아 VLC로 실시간 스트리밍 실행**
2. **yt-dlp 검색 기능을 활용한 영상 검색 제공**

---

## 기능 요구사항

### 1. 스트리밍 실행

* **입력**: 전체 YouTube 영상 URL

  * 예: `https://www.youtube.com/watch?v=zPhICi6IZ_4&t=2536s`
* **처리**:

  * Git Bash 환경에서 다음 명령 실행

    ```bash
    yt-dlp -o - "<url>" | vlc -
    ```
  * Python에서 `subprocess.Popen`으로 실행
* **출력**: VLC 플레이어가 해당 영상 스트리밍 시작

### 2. 영상 검색

* **입력**: 검색어 문자열
* **처리**:

  * `yt-dlp "ytsearch10:<query>" --dump-json` 명령 실행
  * 결과를 JSON으로 파싱
* **출력**:

  ```json
  [
    {"title": "영상 제목", "url": "https://youtube.com/watch?v=..."},
    ...
  ]
  ```
