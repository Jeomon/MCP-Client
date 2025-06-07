from src.client import Client
import asyncio

async def main():
    client=Client.from_config_file("./mcp_servers/config.json")
    session1=await client.create_session('time-mcp')
    tools_list1=await session1.tools_list()
    print(tools_list1)
    await client.close_session('time-mcp')

if __name__ == "__main__":
    asyncio.run(main())

# from mcp.client.sse import sse_client
# from mcp.client.session import ClientSession

# async def main():
#     async with sse_client(url="http://localhost:8081/sse") as (read_stream, write_stream):
#         async with ClientSession(read_stream, write_stream) as session:
#             info=await session.initialize()
#             tools_list=await session.list_tools()
#             print(tools_list)


# if __name__ == "__main__":
#     import asyncio
#     asyncio.run(main())