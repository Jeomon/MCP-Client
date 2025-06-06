from src.transport.stdio import StdioTransport,StdioServerParams
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
    raise ValueError(f'Invalid server configuration: {server_config}')


def is_sse_transport(server_config:dict[str,Any])->bool:
    return 'url' in server_config

def is_stdio_transport(server_config:dict[str,Any])->bool:
    return 'command' in server_config and 'args' in server_config
    