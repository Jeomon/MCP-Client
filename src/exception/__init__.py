
class MCPError(Exception):
    '''JSON-RPC protocol error'''
    def __init__(self, code:int, message:str):
        self.code = code
        self.message = message
        super().__init__(f'JSON-RPC Error {code}: {message}')