from src.mcp.transport.stdio import StdioTransport,StdioServerParams
from src.mcp.transport.streamable_http import StreamableHTTPTransport
from src.mcp.transport.websocket import WebSocketTransport
from src.mcp.transport.sse import SSETransport
from src.mcp.transport.base import BaseTransport
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
    elif is_stdio_transport(server_config):
        params=StdioServerParams(**server_config)
        return StdioTransport(params=params)
    elif is_streamable_http_transport(server_config):
        return StreamableHTTPTransport(**server_config)
    elif is_websocket_transport(server_config):
        return WebSocketTransport(**server_config)
    else:
        raise ValueError(f'Invalid server configuration: {server_config}')


def is_sse_transport(server_config:dict[str,Any])->bool:
    return 'url' in server_config and 'sse' in server_config.get('url')

def is_streamable_http_transport(server_config:dict[str,Any])->bool:
    return 'url' in server_config and 'mcp' in server_config.get('url')

def is_stdio_transport(server_config:dict[str,Any])->bool:
    return 'command' in server_config and 'args' in server_config

def is_websocket_transport(server_config:dict[str,Any])->bool:
    return 'url' in server_config and 'ws' in server_config.get('url')
    