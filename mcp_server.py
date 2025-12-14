from fastmcp import FastMCP
from fastapi import FastAPI


# IMPORTANT: server name must match what OpenAI uses
mcp = FastMCP("local-fastmcp", auth=None)

@mcp.tool()
def ping() -> str:
    """
    Simple health-check tool.
    """
    return "pong"

@mcp.tool()
def add(a: int, b: int) -> int:
    """
    Adds two integers.
    """
    print("MCP add called")
    return a + b


@mcp.tool()
def subtract(a: int, b: int) -> int:
    """
    Subtracts two integers.

    """
    print("MCP subtract called")
    return a - b



mcp_app = mcp.http_app(path="/mcp")
app = FastAPI(lifespan=mcp_app.lifespan)
app.mount("/", mcp_app)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=8000)
