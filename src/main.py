#!/usr/bin/env python3
import asyncio
import json
from mcp.server import Server
from mcp.types import Tool, TextContent
from streaming import stream_youtube_video
from search import search_youtube_videos


app = Server("yt2vlc-mcp")


@app.list_tools()
async def list_tools():
    return [
        Tool(
            name="stream_youtube",
            description="YouTube 영상을 VLC 플레이어로 스트리밍합니다",
            inputSchema={
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "YouTube 영상 URL (전체 URL)"
                    }
                },
                "required": ["url"]
            }
        ),
        Tool(
            name="search_youtube",
            description="YouTube에서 영상을 검색합니다",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "검색할 키워드"
                    }
                },
                "required": ["query"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "stream_youtube":
        url = arguments.get("url")
        if not url:
            return [TextContent(type="text", text="URL이 필요합니다.")]

        if "youtube.com" not in url and "youtu.be" not in url:
            return [TextContent(type="text", text="유효한 YouTube URL이 아닙니다.")]

        try:
            result = stream_youtube_video(url)
            return [TextContent(
                type="text",
                text=f"스트리밍 시작됨 - PID: {result['pid']}, 상태: {result['status']}"
            )]
        except Exception as e:
            return [TextContent(type="text", text=f"스트리밍 실행 실패: {str(e)}")]

    elif name == "search_youtube":
        query = arguments.get("query")
        if not query:
            return [TextContent(type="text", text="검색어가 필요합니다.")]

        try:
            videos = search_youtube_videos(query)
            result_text = "검색 결과:\n\n"
            for i, video in enumerate(videos, 1):
                result_text += f"{i}. {video['title']}\n   URL: {video['url']}\n\n"

            return [TextContent(type="text", text=result_text)]
        except Exception as e:
            return [TextContent(type="text", text=f"검색 실행 실패: {str(e)}")]

    else:
        return [TextContent(type="text", text=f"알 수 없는 도구: {name}")]


async def main():
    from mcp.server.stdio import stdio_server

    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())