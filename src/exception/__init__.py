
class MCPError(Exception):
    '''MCP Protocol Error'''
    def __init__(self, code:int, message:str):
        self.code = code
        self.message = message
        super().__init__(f'JSON-RPC Error {code}: {message}')