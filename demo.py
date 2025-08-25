import asyncio
import json
from asyncio.subprocess import Process
from typing import Any, AsyncGenerator, Dict, Optional

class StdioTransport:
    def __init__(self, command: str, args: list[str] = []):
        self.command = command
        self.args = args
        self.process: Optional[Process] = None
        self.is_connected = False

    async def connect(self):
        """
        Start a subprocess and connect to its stdin/stdout.
        """
        self.process = await asyncio.create_subprocess_exec(
            self.command,
            *self.args,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        self.is_connected = True

    async def disconnect(self):
        """
        Terminate the subprocess gracefully.
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

    async def send_message(self, message: Dict[str, Any]):
        """
        Send a JSON message to the subprocess over stdin.
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
        Receive a single JSON message from the subprocess.
        Returns None if the process is closed.
        """
        if not self.process or not self.process.stdout or not self.is_connected:
            raise RuntimeError("Transport is not connected")

        try:
            line = await self.process.stdout.readline()
            if not line:  # process ended
                return None
            message = json.loads(line.decode("utf-8"))
            return message
        except asyncio.CancelledError:
            return None
        except Exception as e:
            print(f"Error receiving message: {e}")
            return None


async def main():
    transport = StdioTransport(**{
            "command": "uv",
            "args": [
                "--directory",
                "D:\\Personal Projects\\Windows-MCP",
                "run",
                "main.py"
            ]
        })
    await transport.connect()

    # Send a message
    await transport.send_message({"jsonrpc":"2.0","id":"ec841147-0927-4e84-9e5a-9ca22aa8a7c0","params":{"protocolVersion":"2024-11-05","capabilities":{"experimental":{},"roots":{"listChanged":True}},"clientInfo":{"name":"MCP Client","version":"0.1.0"}},"method":"initialize"})

    response = await transport.receive_message()
    print("Got single response:", response)

    await transport.disconnect()

if __name__ == "__main__":
    asyncio.run(main())