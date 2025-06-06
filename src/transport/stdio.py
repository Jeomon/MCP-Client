from src.types.json_rpc import JSONRPCRequest, JSONRPCResponse, JSONRPCNotification
from src.types.stdio import StdioServerParams
from src.transport.base import BaseTransport
from asyncio.subprocess import Process
from typing import Any
import asyncio
import json

class StdioTransport(BaseTransport):
    """
    Stdio transport for MCP

    Communicates with the MCP server via stdin and stdout of subprocess
    """
    def __init__(self,params:StdioServerParams):
        self.params=params
        self.process:Process = None
        self.listen_task:asyncio.Task = None
        self.queue:dict[str,asyncio.Queue[JSONRPCResponse]]={}

    async def connect(self)->None:
        command=self.params.command
        args=self.params.args
        self.process=await asyncio.create_subprocess_exec(command,*args,stdin=asyncio.subprocess.PIPE,stdout=asyncio.subprocess.PIPE,stderr=asyncio.subprocess.PIPE)
        self.listen_task=asyncio.create_task(self.listen())

    async def send_request(self, request:JSONRPCRequest)->JSONRPCResponse:
        id=request.id
        self.queue[id]=asyncio.Queue()
        try:
            self.process.stdin.write((json.dumps(request.model_dump()) + '\n').encode())
            await self.process.stdin.drain()

            queue=self.queue.get(id)
            response = await queue.get()
        except asyncio.TimeoutError:
            raise Exception("Request timed out")
        except Exception as e:
            raise Exception(f"Error: {e}")
        finally:
            self.queue.pop(id)
        return response
    
    async def send_notification(self, notification:JSONRPCNotification)->None:
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
        while True:
            try:
                line=await self.process.stdout.readline()
                if not line:
                    break # If the process is closed/cancelled
                try:
                    message = JSONRPCResponse.model_validate(json.loads(line.decode().strip()))
                except json.JSONDecodeError:
                    print(f"Invalid JSON received: {line}")
                
                id=message.id
                if id and id in self.queue.keys():
                    queue=self.queue.get(id)
                    await queue.put(message)
            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"Error: {e}")

    async def disconnect(self):
        """
        Stop the MCP server process.
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
