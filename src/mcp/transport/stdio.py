from src.mcp.types.json_rpc import JSONRPCRequest, JSONRPCResponse, JSONRPCError, Error, JSONRPCNotification
from src.mcp.transport.utils import get_default_environment
from src.mcp.types.stdio import StdioServerParams
from src.mcp.transport.base import BaseTransport
from asyncio.subprocess import Process
from src.mcp.exception import MCPError
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
        self.process:Process = None
        self.listen_task:asyncio.Task = None
        self.request_queue:asyncio.Queue[JSONRPCRequest] = asyncio.Queue()
        self.response_queue:dict[str,asyncio.Queue[JSONRPCResponse|JSONRPCError]]={}

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
        self.listen_task=asyncio.create_task(self.listen())

    async def receive_request(self)-> JSONRPCRequest|None:
        '''
        Receive a JSON RPC request from the MCP server

        Returns:
            JSON RPC request object
        '''
        if self.request_queue.empty():
            return None
        return await self.request_queue.get()

    async def receive_response(self,id:str|int)-> JSONRPCResponse|None:
        '''
        Receive a JSON RPC response from the MCP server

        Returns:
            JSON RPC response object
        '''
        queue=self.response_queue.get(id)
        if queue is None:
            raise ValueError(f"No response queue found for id: {id}")
        response = await queue.get()
        if isinstance(response,JSONRPCError):
            error=response.error
            raise MCPError(code=error.code,message=error.message)
        return response

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
        id=request.id
        self.response_queue[id]=asyncio.Queue()
        try:
            # send the request to the MCP server
            self.process.stdin.write((json.dumps(request.model_dump()) + '\n').encode())
            await self.process.stdin.drain()
            response=await self.receive_response(id=id)
        except asyncio.TimeoutError:
            raise Exception("Request timed out")
        except Exception as e:
            raise Exception(f"Error: {e}")
        finally:
            self.response_queue.pop(id)
        return response

    async def send_response(self, response:JSONRPCResponse)->None:
        '''
        Send a JSON RPC response to the MCP server

        Args:
            response: JSON RPC response object
        '''
        self.process.stdin.write((json.dumps(response.model_dump()) + '\n').encode())
        await self.process.stdin.drain()

    async def send_notification(self, notification:JSONRPCNotification)->None:
        '''
        Send a JSON RPC notification to the MCP server

        Args:
            notification: JSON RPC notification object
        '''
        try:
            self.process.stdin.write((json.dumps(notification.model_dump()) + '\n').encode())
            await self.process.stdin.drain()
        except asyncio.TimeoutError:
            raise Exception("Request timed out")
        except Exception as e:
            raise Exception(f"Error: {e}")
        
    async def listen(self):
        '''
        Listens for JSON RPC messages from Stdio Server
        '''
        buffer=bytearray()
        while True:
            try:
                # Receive data from the MCP server
                chunk=await self.process.stdout.read(1024)
                if not chunk:
                    break # If the process is closed/cancelled
                buffer.extend(chunk)
                try:
                    content:dict=json.loads(buffer.decode().strip())
                    if 'id' in content and 'result' in content:
                        message = JSONRPCResponse.model_validate(content)
                    elif 'id' in content and 'error' in content:
                        id=content.get('id')
                        error=Error.model_validate(content.get('error'))
                        message=JSONRPCError(id=id,error=error,message=error.message)
                    elif 'id' in content or 'params' in content:
                        message=JSONRPCRequest.model_validate(content)
                    elif 'id' not in content or 'params' in content:
                        message=JSONRPCNotification.model_validate(content)
                    buffer.clear()  # Reset buffer after successful parse
                except json.JSONDecodeError:
                    continue # Continue reading until a complete JSON object is received
                id=message.id
                queue=self.response_queue.get(id)
                if queue is not None:
                    await queue.put(message)
                else:
                    if id is not None:
                        await self.request_queue.put(message)
            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"Error: {e}")

    async def disconnect(self):
        """
        Disconnect from the MCP server process.
        """
        if self.listen_task:
            self.listen_task.cancel()
            try:
                await self.listen_task
            except asyncio.CancelledError:
                pass
            finally:
                self.listen_task=None
        if self.process and self.process.stdin:
            try:
                self.process.stdin.write_eof()
            except Exception:
                pass
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
            self.process = None
