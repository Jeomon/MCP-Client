from mcp.server.sse import SseServerTransport
from starlette.applications import Starlette
import starlette
import starlette.requests
from starlette.routing import Route, Mount
from starlette.responses import StreamingResponse
from mcp.server.fastmcp import FastMCP
from datetime import datetime
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

mcp = FastMCP("example-server")
sse = SseServerTransport("/messages/")

@mcp.tool(name="Time-Tool", description="Returns the current time")
def time_tool():
    return "The current time is: " + datetime.now().strftime("%H:%M:%S")

async def handle_sse(request: starlette.requests.Request):
    """Handle SSE connections for the MCP server."""
    try:
        async with sse.connect_sse(
            request.scope, 
            request.receive, 
            request._send
        ) as (read_stream, write_stream):
            await mcp._mcp_server.run(
                read_stream=read_stream, 
                write_stream=write_stream, 
                initialization_options=mcp._mcp_server.create_initialization_options()
            )
    except Exception as e:
        logger.error(f"SSE connection error: {e}", exc_info=True)
        raise e

# Create Starlette app with proper routing
starlette_app = Starlette(
    routes=[
        Route("/sse", handle_sse, methods=["GET"]),  # Use Route, not Mount
        Mount("/messages", app=sse.handle_post_message),  # Mount is correct for ASGI apps
    ]
)

from fastapi import FastAPI,Request,Response

app = FastAPI()
app.mount("/", app=starlette_app)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8081)