from src.mcp.types.json_rpc import JSONRPCRequest, JSONRPCError, Error, JSONRPCResponse
from src.mcp.transport.base import BaseTransport
from httpx import AsyncClient, Limits
from httpx_sse import aconnect_sse
from src.mcp.exception import MCPError
from urllib.parse import urljoin
from typing import Optional
import asyncio
import json


class SSETransport(BaseTransport):
    '''
    SSE Transport for MCP

    Communicates with the MCP server via Server-Sent Events
    '''
    def __init__(self,url:str,headers:Optional[dict[str,str]]=None):
        self.url=url
        self.session_url=None
        self.headers=headers or {}
        self.client:AsyncClient=None
        self.listen_task:asyncio.Task=None
        self.ready_event=asyncio.Event()
        self.queue:dict[str,asyncio.Queue[JSONRPCResponse|JSONRPCError]]={}

    async def connect(self):
        '''
        Create a SSE Client
        '''
        self.client=AsyncClient(timeout=30,headers=self.headers,limits=Limits(max_connections=10))
        self.listen_task=asyncio.create_task(self.listen())
        await self.ready_event.wait()

    async def send_request(self, request:JSONRPCRequest)->JSONRPCResponse|JSONRPCError:
        '''
        Send a JSON RPC request to the MCP server

        Args:
            request: JSON RPC request object

        Returns:
            JSON RPC response object
        
        Raises:
            MCPError: If the request fails
        '''
        headers={
            **self.headers,
            "Content-Type": "application/json",
        }
        json_payload=request.model_dump()
        await self.client.post(self.session_url,headers=headers,json=json_payload)
        queue=self.queue.get(self.session_url)
        response = await queue.get()
        if isinstance(response,JSONRPCError):
            error=response.error
            raise MCPError(code=error.code,message=error.message)
        return response

    async def send_notification(self, notification:JSONRPCResponse):
        '''
        Send a JSON RPC notification to the MCP server

        Args:
            notification: JSON RPC notification object
        '''
        headers={
            **self.headers,
            "Content-Type": "application/json",
        }
        json_payload=notification.model_dump()
        await self.client.post(self.session_url,headers=headers,json=json_payload)
        
    async def listen(self):
        '''
        Listen for JSON RPC messages from the MCP
        '''
        async with aconnect_sse(self.client, 'GET', self.url) as iter:
            async for obj in iter.aiter_sse():
                try:
                    match obj.event:
                        case 'endpoint':
                            self.session_url=urljoin(self.url,obj.data)
                            self.queue[self.session_url]=asyncio.Queue()
                            self.ready_event.set()
                        case 'message':
                            queue=self.queue.get(self.session_url)
                            content:dict=json.loads(obj.data)
                            if 'result' in content:
                                message = JSONRPCResponse.model_validate(content)
                            elif 'error' in content:
                                error=Error.model_validate(content.get('error'))
                                message=JSONRPCError(id=content.get('id'),error=error,message=error.message)
                            await queue.put(message)
                        case _:
                            pass
                except Exception as e:
                    print(f"Error: {e}")
                        
    async def disconnect(self):
        '''
        Disconnect from the MCP server
        '''
        if self.listen_task:
            self.listen_task.cancel()
            try:
                await self.listen_task
            except asyncio.CancelledError:
                pass
            finally:
                self.listen_task=None

        if self.client:
            await self.client.aclose()
            self.client=None
