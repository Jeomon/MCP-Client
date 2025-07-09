from src.mcp.types.json_rpc import JSONRPCRequest, JSONRPCResponse, JSONRPCError, Error
from src.mcp.exception import MCPError
from typing import Optional, Dict
import websockets
import asyncio
import json

class WebSocketTransport:
    def __init__(self, url: str, headers: Optional[dict[str, str]] = None):
        self.url = url
        self.headers = headers or {}
        self.websocket: Optional[websockets.ClientConnection] = None
        self.listen_task: Optional[asyncio.Task] = None
        self.queue: Dict[str, asyncio.Queue[JSONRPCResponse | JSONRPCError]] = {}

    async def connect(self):
        '''
        Create a WebSocket Client
        '''
        self.websocket = await websockets.connect(self.url, additional_headers=self.headers, subprotocols=["mcp"])
        self.listen_task = asyncio.create_task(self.listen())

    async def listen(self):
        '''
        Listen for JSON RPC messages from the MCP
        '''
        try:
            async for data in self.websocket:
                try:
                    content:dict = json.loads(data)
                    id=content.get("id")
                    if "result" in content:
                        message = JSONRPCResponse.model_validate(content.get("result"))
                    elif "error" in content:
                        error = Error.model_validate(content.get("error"))
                        message = JSONRPCError(id=id, error=error)
                    if id in self.queue:
                        queue=self.queue.get(id)
                        await queue.put(message)
                except Exception as e:
                    print(f"Error parsing message: {e}")
        except websockets.exceptions.ConnectionClosed:
            print("WebSocket closed.")

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
        id=request.id
        self.queue[id] = asyncio.Queue()
        await self.websocket.send(json.dumps(request.model_dump()))
        queue=self.queue.get(id)
        response = await queue.get()
        if isinstance(response, JSONRPCError):
            error=response.error
            raise MCPError(code=error.code, message=error.message)
        return response

    async def send_notification(self, notification: JSONRPCRequest):
        '''
        Send a JSON RPC notification to the MCP server

        Args:
            notification: JSON RPC notification object
        '''
        await self.websocket.send(json.dumps(notification.model_dump()))

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

        if self.websocket:
            await self.websocket.close()
