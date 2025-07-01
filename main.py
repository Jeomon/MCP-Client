from src.mcp.client import Client
import asyncio

async def main():
    client=Client.from_config_file('./mcp_servers/config.json')
    session=await client.create_session('windows-mcp')
    state=await session.tools_call('State-Tool',{'use_vision':True})
    print(state.content[1].data[:100])
    await client.close_session('windows-mcp')

if __name__ == '__main__':
    asyncio.run(main())
