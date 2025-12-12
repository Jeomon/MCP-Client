from src.mcp.client.service import MCPClient
from src.mcp.types.tools import CallToolRequestParams
from src.mcp.logger import get_logger, configure_logging
import asyncio

# Configure logging
configure_logging(level="INFO")
logger = get_logger(__name__)

async def main():
    client=MCPClient.from_config_file('./mcp_servers/config.json')
    session=await client.create_session('calculator-mcp')
    logger.info("Init Result: %s", session.get_initialize_result())
    # sleep(5)
    logger.info("Tools: %s", await session.tools_list())
    result = await session.tools_call(CallToolRequestParams(name='add', arguments={'a':10,'b':20}))
    logger.info("Tool Result: %s", result)
    await client.close_session('calculator-mcp')

if __name__ == '__main__':
    asyncio.run(main())
