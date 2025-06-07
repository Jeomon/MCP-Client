from mcp.server.fastmcp import FastMCP

mcp=FastMCP("Streamable HTTP Server")

@mcp.tool("Greet-Tool")
def greet_tool(name: str) -> str:
    return f"Hello, {name}!"

if __name__ == "__main__":
    mcp.run(transport="streamable-http")