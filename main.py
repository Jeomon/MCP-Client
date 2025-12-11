from src.mcp.client.service import MCPClient
import asyncio
from src.mcp.types.tools import ToolsListRequest, ToolRequest

async def main():
    client=MCPClient.from_config_file('./mcp_servers/config.json')
    session=await client.create_session('calculator-mcp')
    print("Init Result:", session.get_initialize_result())
    # sleep(5)
    print("Tools:", await session.tools_list(ToolsListRequest()))
    result = await session.tools_call(ToolRequest(name='add',arguments={'a':10,'b':20}))
    print("Tool Result:", result)
    await client.close_session('calculator-mcp')

if __name__ == '__main__':
    asyncio.run(main())
