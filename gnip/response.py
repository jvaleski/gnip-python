class Response(object):
    """Gnip server response object.
    
    code:   integer representing the response code
    result: string representing the response

    """
    def __init__(self, code, result):
        self.code = code
        self.result = result