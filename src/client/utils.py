from src.transport.stdio import StdioTransport,StdioServerParams
from src.transport.streamable_http import StreamableHTTPTransport
from src.transport.sse import SSETransport
from src.transport.base import BaseTransport
from typing import Any

def create_transport_from_server_config(server_config:dict[str,Any])->BaseTransport:
    '''
    Create a transport based on the server configuration

    Args:
        server_config: The server configuration

    Returns:
        The transport instance for the server
    '''
    if is_sse_transport(server_config):
        return SSETransport(**server_config)
    if is_stdio_transport(server_config):
        params=StdioServerParams(**server_config)
        return StdioTransport(params=params)
    if is_streamable_http_transport(server_config):
        return StreamableHTTPTransport(**server_config)
    
    raise ValueError(f'Invalid server configuration: {server_config}')


def is_sse_transport(server_config:dict[str,Any])->bool:
    return 'url' in server_config and 'sse' in server_config.get('url')

def is_streamable_http_transport(server_config:dict[str,Any])->bool:
    return 'url' in server_config and 'mcp' in server_config.get('url')

def is_stdio_transport(server_config:dict[str,Any])->bool:
    return 'command' in server_config and 'args' in server_config
    