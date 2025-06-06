from src.transport.stdio import StdioTransport
from src.types.stdio import StdioServerParams
from src.message.initialize import send_initialize
from src.message.tools import send_tools_list,send_tools_call,ToolRequest
import asyncio

async def main():
    params=StdioServerParams(command="python",args=["./mcp_servers/calculator_mcp.py"])
    stdio_transport=StdioTransport(params=params)
    await stdio_transport.connect()
    initialize_result=await send_initialize(transport=stdio_transport)
    print(initialize_result)
    await stdio_transport.disconnect()

if __name__ == "__main__":
    asyncio.run(main())