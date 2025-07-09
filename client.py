import asyncio

from src.mcp.client import MCPClient

async def main():
    client=MCPClient()
    client.add_server('test',{
                "command": "python",
                "args": ["./test.py"]
            })

    await client.create_session('test')
    await asyncio.sleep(5)
    await client.close_session('test')


if __name__ == "__main__":
    asyncio.run(main())
