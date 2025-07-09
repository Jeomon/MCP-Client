from src.mcp.server.transport.stdio import StdioTransport
import asyncio

async def main():
    transport = StdioTransport()
    await asyncio.gather(
        transport.listen(),
        transport.handle_request()
    )

if __name__ == "__main__":
    asyncio.run(main())