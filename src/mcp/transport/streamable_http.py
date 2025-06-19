from src.mcp.types.json_rpc import JSONRPCRequest, JSONRPCNotification, JSONRPCResponse, JSONRPCError, Error, Method
from src.mcp.transport.base import BaseTransport
from httpx import AsyncClient, Limits
from typing import Optional
import json

class StreamableHTTPTransport(BaseTransport):
    def __init__(self, url: str, headers: Optional[dict[str, str]] = None):
        self.url = url
        self.headers = headers or{}
        self.mcp_session_id = None
        self.protocol_version=None
        self.client: AsyncClient = None

    async def connect(self):
        '''
        Create a Http Client
        '''
        self.client = AsyncClient(timeout=30, headers=self.headers, limits=Limits(max_connections=10))

    async def send_request(self, request: JSONRPCRequest) -> JSONRPCResponse | JSONRPCError:
        '''
        Send a JSON RPC request to the MCP server

        Args:
            request: JSON RPC request object

        Returns:
            JSON RPC response object

        Raises:
            MCPError: If the request fails
        '''
        headers = {**self.headers,'Content-Type': 'application/json', 'Accept': 'application/json, text/event-stream'}
        if headers.get('mcp-session-id') is None and self.mcp_session_id is not None:        
            headers['mcp-session-id'] = self.mcp_session_id
        if self.protocol_version is not None:
            headers['mcp-protocol-version'] = self.protocol_version
        json_payload = request.model_dump()
        message = None
        async with self.client.stream('POST',self.url, headers=headers, json=json_payload) as response:
            if self.mcp_session_id is None:
                self.mcp_session_id=response.headers.get('mcp-session-id')
            buffer=bytearray()
            async for chunk in response.aiter_bytes(50):
                buffer.extend(chunk)
                try:
                    data=buffer.decode().strip()
                    content:dict=json.loads(data[21:].strip())
                    if 'result' in content:
                        message = JSONRPCResponse.model_validate(content)
                        if request.method == Method.INITIALIZE:
                            self.protocol_version=message.result.get('protocolVersion')
                    elif 'error' in content:
                        error = Error.model_validate(content.get('error'))
                        message = JSONRPCError(id=content.get('id'), error=error, message=error.message)
                    buffer.clear()  # Clear the buffer after processing
                except json.JSONDecodeError:
                    continue
        return message

    async def send_notification(self, notification: JSONRPCNotification):
        '''
        Send a JSON RPC notification to the MCP server

        Args:
            notification: JSON RPC notification object
        '''
        headers = {**self.headers,'Content-Type': 'application/json', 'Accept': 'application/json, text/event-stream'}
        if headers.get('mcp-session-id') is None:              
            headers['mcp-session-id'] = self.mcp_session_id
        json_payload = notification.model_dump()
        await self.client.post(self.url, headers=headers, json=json_payload)          

    async def disconnect(self):
        '''
        Disconnect from the MCP server
        '''
        headers = {**self.headers,'Content-Type': 'application/json', 'Accept': 'application/json, text/event-stream'}
        if headers.get('mcp-session-id') is None:        
            headers['mcp-session-id'] = self.mcp_session_id
        await self.client.delete(self.url, headers=headers)
        if self.client:
            await self.client.aclose()
            self.client = None
        self.mcp_session_id = None