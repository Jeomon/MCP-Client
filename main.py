from src.mcp.client.service import MCPClient
from time import sleep
import asyncio

async def main():
    client=MCPClient.from_config_file('./mcp_servers/config.json')
    session=await client.create_session('windows-mcp')
    print(session.get_initialize_result())
    # sleep(5)
    response=await session.tools_call(tool_name="State-Tool")
    print(response.content[0].text)
    await client.close_session('windows-mcp')

if __name__ == '__main__':
    asyncio.run(main())
