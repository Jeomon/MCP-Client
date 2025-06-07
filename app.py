from src.client import Client
import asyncio

async def main():
    client=Client.from_config_file("./mcp_servers/config.json")
    session1=await client.create_session('time-mcp')
    session2=await client.create_session('windows-mcp')
    tools_list1=await session1.tools_list()
    print(tools_list1)
    tool_result=await session1.tools_call('Time-Tool',{})
    print(tool_result)
    tools_list2=await session2.tools_list()
    print(tools_list2)
    await client.close_session('windows-mcp')
    await client.close_session('time-mcp')

if __name__ == "__main__":
    asyncio.run(main())