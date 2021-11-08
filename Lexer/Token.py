class Token():
    """
        A simple Token class
        inputs: type: str, string: str
        outputs: get_type() -> str, get_string() -> str
    """

    def __init__(self, type: str, string: str):
        self._type = type
        self._string = string

    def get_type(self) -> str:
        return self._type

    def get_string(self) -> str:
        return self._string

    def set_type(self, new_type:str) -> None:
        self._type = new_type

    def set_string(self, new_string:str) -> None:
        self._string = new_string

    def __eq__(self, other) -> bool:
        if not isinstance(other,Token):
            return False

        else:
            if self._type == other.get_type() and self._string == other.get_string():
                return True
            else:
                return False

    def __repr__(self) -> str:
        return "Token(type: {}, string: {})".format(self._type, self._string)