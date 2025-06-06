from src.transport.stdio import StdioTransport
from src.types.stdio import StdioServerParams
from src.session import Session
import asyncio

async def main():
    params=StdioServerParams(command="python",args=["./mcp_servers/calculator_mcp.py"])
    stdio_transport=StdioTransport(params=params)
    session=Session(transport=stdio_transport)
    await session.connect()
    initialize_result=await session.initialize()
    print(initialize_result)
    await session.disconnect()

if __name__ == "__main__":
    asyncio.run(main())