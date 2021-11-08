class Parser_Syntax_Error(BaseException):
    """Exception raised because the Parser found a Syntax Error

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message: str) -> None:
        self.message = 'SyntaxError: ' + message