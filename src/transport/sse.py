from src.types.json_rpc import JSONRPCRequest, JSONRPCError, JSONRPCResponse
from src.transport.base import BaseTransport
from httpx import AsyncClient, Limits
from typing import Optional
import json

class SSETransport(BaseTransport):
    '''
    SSE Transport for MCP

    Communicates with the MCP server via Server-Sent Events
    '''
    def __init__(self,url:str,headers:Optional[dict[str,str]]=None):
        self.url=url
        self.headers=headers
        self.client=None

    async def connect(self):
        '''
        Create a Http Client
        '''
        self.client=AsyncClient(timeout=30,headers=self.headers,limits=Limits(max_connections=10))

    async def disconnect(self):
        '''
        Close the Http Client
        '''
        if self.client:
            await self.client.aclose()

    async def send_request(self, request:JSONRPCRequest):
        headers={
            **self.headers,
            "Content-Type": "application/json",
            "Accept": "text/event-stream"
        }
        id=request.id
        json_payload=request.model_dump_json()
        async with self.client.stream("POST",self.url,headers=headers,json=json_payload) as response:
            response.raise_for_status()
            async for line in response.aiter_lines():
                if line.startswith("data: "):
                    try:
                        data:dict=json.loads(line[6:])
                        if data.get("id")==id:
                            if data.get("result"):
                                return JSONRPCResponse.model_validate(data)
                            elif data.get("error"):
                                return JSONRPCError.model_validate(data)
                    except json.JSONDecodeError:
                        print(f"Invalid JSON received: {line}")
        raise Exception(f"Request timed out for request id: {id}")

    async def send_notification(self, notification:JSONRPCResponse):
        headers={
            **self.headers,
            "Content-Type": "application/json",
        }
        json_payload=notification.model_dump_json()
        async with self.client.post(self.url,headers=headers,json=json_payload) as response:
            response.raise_for_status()

