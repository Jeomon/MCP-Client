from src.mcp.client import MCPClient
from time import sleep
import asyncio

async def main():
    client=MCPClient.from_config_file('./mcp_servers/config.json')
    session=await client.create_session('greet-mcp')
    print(session.get_initialize_result())
    # sleep(5)
    response=await session.tools_call(tool_name="Greet-Tool",name="John")
    print(response.content[0].text)
    await client.close_session('greet-mcp')

if __name__ == '__main__':
    asyncio.run(main())
