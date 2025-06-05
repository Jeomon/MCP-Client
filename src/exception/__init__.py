

class MCPError(Exception):
    '''Base error for MCP related issues'''
    pass

class MCPConnectionError(MCPError):
    '''Error connecting to the MCP server'''
    pass

class MCPTimeoutError(MCPError):
    '''Timeout at waiting for response from MCP server'''
    pass

class MCPToolError(MCPError):
    '''Error while executing a tool in the MCP server'''
    pass

class JSONRPCError(MCPError):
    '''JSON-RPC protocol error'''
    def __init__(self, code:int, message:str):
        self.code = code
        self.message = message
        super().__init__(f'JSON-RPC Error {code}: {message}')