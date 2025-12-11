from src.mcp.client.service import MCPClient
from time import sleep
import asyncio

async def main():
    client=MCPClient.from_config_file('./mcp_servers/config.json')
    session=await client.create_session('code-mcp')
    print(session.get_initialize_result())
    # sleep(5)
    print(await session.tools_list())
    print(await session.tools_call('bash_tool',**{'cmd':'uname -a' }))
    await client.close_session('code-mcp')

if __name__ == '__main__':
    asyncio.run(main())
