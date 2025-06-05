from src.transport.stdio import StdioTransport
from src.types.stdio import StdioServerParams
from src.message.initialize import send_initialize
from src.message.tools import send_tools_list,send_tools_call,ToolRequest
import asyncio

async def main():
    params=StdioServerParams(command="python",args=["./mcp_servers/calculator_mcp.py"])
    stdio_transport=StdioTransport(params=params)
    await stdio_transport.connect()
    await send_initialize(transport=stdio_transport)
    response=await send_tools_call(transport=stdio_transport,tool_request=ToolRequest(name='add',arguments={"a":1,"b":2}))
    print(response)
    await stdio_transport.disconnect()

if __name__ == "__main__":
    asyncio.run(main())