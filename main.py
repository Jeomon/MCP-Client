from src.mcp.client import MCPClient
import asyncio

async def main():
    client=MCPClient.from_config_file('./mcp_servers/config.json')
    session=await client.create_session('windows-mcp')
    state=await session.tools_call('State-Tool',{'use_vision':False})
    print(state.content)
    await client.close_session('windows-mcp')

if __name__ == '__main__':
    asyncio.run(main())
