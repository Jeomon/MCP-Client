from src.client import Client
import asyncio

async def main():
    client=Client.from_config_file("./mcp_servers/config.json")
    session=await client.create_session('calculator')
    tools_list=await session.tools_list()
    print(tools_list)
    await client.close_session("calculator")


if __name__ == "__main__":
    asyncio.run(main())