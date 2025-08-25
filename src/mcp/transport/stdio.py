from src.mcp.types.json_rpc import JSONRPCRequest, JSONRPCResponse, JSONRPCNotification
from src.mcp.transport.utils import get_default_environment
from src.mcp.types.stdio import StdioServerParams
from src.mcp.transport.base import BaseTransport
from asyncio.subprocess import Process
from typing import Optional,Dict,Any
import asyncio
import json
import sys

class StdioTransport(BaseTransport):
    """
    Stdio Transport for MCP

    Communicates with the MCP server via stdin and stdout of subprocess
    """
    def __init__(self,params:StdioServerParams):
        self.params=params
        self.process:Optional[Process] = None
        self.is_connected = False

    async def connect(self)->None:
        '''
        Create a Stdio Client
        '''
        command=self.params.command
        args=self.params.args

        env=get_default_environment() if self.params.env is None else {**get_default_environment(),**self.params.env}
        if sys.platform=='win32' and command=='npx':
            command='cmd'
            args=['/c','npx',*args]

        self.process=await asyncio.create_subprocess_exec(command,*args,env=env,stdin=asyncio.subprocess.PIPE,stdout=asyncio.subprocess.PIPE,stderr=asyncio.subprocess.PIPE,start_new_session=True)
        self.is_connected = True

    async def disconnect(self):
        """
        Disconnect from the MCP server process.
        """
        if self.process and self.is_connected:
            if self.process.stdin:
                self.process.stdin.close()
                if hasattr(self.process.stdin, "wait_closed"):
                    await self.process.stdin.wait_closed()
            self.process.terminate()
            try:
                await asyncio.wait_for(self.process.wait(), timeout=5)
            except asyncio.TimeoutError:
                print("Process did not terminate in time; killing it.")
                self.process.kill()
                await self.process.wait()
            self.is_connected = False
            self.process = None

    async def send_message(self, message: dict):
        """
        Send a JSON RPC message.
        """
        if not self.process or not self.process.stdin or not self.is_connected:
            raise RuntimeError("Transport is not connected")
        try:
            data = json.dumps(message).encode("utf-8") + b"\n"
            self.process.stdin.write(data)
            await self.process.stdin.drain()
        except Exception as e:
            print(f"Error sending message: {e}")

    async def receive_message(self) -> Dict[str, Any] | None:
        """
        Continuously read JSON messages from the subprocess stdout.
        """
        if not self.process or not self.process.stdout or not self.is_connected:
            raise RuntimeError("Transport is not connected")

        buffer = bytearray()
        while True:
            try:
                chunk = await self.process.stdout.read(1024)
                if not chunk:  # process ended
                    return None

                buffer.extend(chunk)

                try:
                    content = json.loads(buffer.decode().strip())
                    return content
                except json.JSONDecodeError:
                    continue
            except asyncio.CancelledError:
                return None
            except Exception as e:
                print(f"Error receiving message: {e}")
                return None

    async def send_request(self, request: JSONRPCRequest) -> JSONRPCResponse | None:
        """
        Send a JSON RPC request and wait for the response.
        """
        await self.send_message(request.model_dump())
        response = await self.receive_message()
        if response:
            return JSONRPCResponse.model_validate(response)
        return None
    
    async def send_response(self, response: JSONRPCResponse) -> None:
        """
        Send a JSON RPC response.
        """
        await self.send_message(response.model_dump())

    async def receive_response(self) -> JSONRPCResponse | None:
        """
        Receive a JSON RPC response.
        """
        response = await self.receive_message()
        if response:
            return JSONRPCResponse.model_validate(response)
        return None

    async def receive_request(self) -> JSONRPCRequest | None:
        """
        Receive a JSON RPC request.
        """
        request = await self.receive_message()
        if request:
            return JSONRPCRequest.model_validate(request)
        return None

    async def send_notification(self, notification: JSONRPCNotification) -> None:
        """
        Send a JSON RPC notification.
        """
        await self.send_message(notification.model_dump())
