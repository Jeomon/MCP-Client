from src.mcp.client.service import MCPClient
from time import sleep
import asyncio

async def main():
    client=MCPClient.from_config_file('./mcp_servers/config.json')
    session=await client.create_session('calculator-mcp')
    print("Init Result:", session.get_initialize_result())
    # sleep(5)
    print("Tools:", await session.tools_list())
    result = await session.tools_call('add',a=10,b=20)
    print("Tool Result:", result)
    await client.close_session('calculator-mcp')

if __name__ == '__main__':
    asyncio.run(main())
