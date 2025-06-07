from src.mcp.types.json_rpc import JSONRPCRequest,JSONRPCResponse,JSONRPCError,JSONRPCNotification
from abc import abstractmethod,ABC
from typing import Any,Dict

class BaseTransport(ABC):
    """
    The abstract class for transport layer of the MCP
    """
    @abstractmethod
    async def connect(self)->None:
        '''
        Establish connection to the MCP server.
        '''
        pass

    @abstractmethod
    async def disconnect(self)->None:
        '''
        Close connection to the MCP server.
        '''
        pass

    @abstractmethod
    async def send_request(self,request:JSONRPCRequest)->JSONRPCResponse|JSONRPCError:
        '''
        Send JSON RPC request to the MCP server.

        Args:
            request: JSONRPCRequest object
        
        Raises:
            TimeoutError: If the request times out
            
            Exception: If the request fails
        '''
        pass

    @abstractmethod
    async def send_notification(self,notification:JSONRPCNotification)->None:
        '''
        Send JSON RPC notification to the MCP server.

        Args:
            notification: JSON RPC notification object
        '''
        pass

