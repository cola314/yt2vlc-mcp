from fastmcp import FastMCP

proxy = FastMCP.as_proxy(
    "http://127.0.0.1:8000/mcp",
    name="yt2vlc Proxy",
)

if __name__ == "__main__":
    proxy.run()
