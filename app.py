from src.client import Client
import asyncio

async def main():
    client=Client.from_config_file("./mcp_servers/config.json")
    await client.create_all_sessions()
    session1=client.get_session("exa-mcp")
    tools_list1=await session1.tools_list()
    print(tools_list1)
    await client.close_all_sessions()

if __name__ == "__main__":
    asyncio.run(main())