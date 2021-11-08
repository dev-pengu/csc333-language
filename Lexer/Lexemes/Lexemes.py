import re

### ======================================== Tokens ======================================== ###

class _Token_Enum():
    def __init__(self) -> None:
        class _Operators():
            def __init__(self) -> None:
                self.Add = "+"
                self.Subtract = "-"
                self.Multiply = "*"
                self.Division = "/"
                self.Power = "**"
                self.Int_Division = "//"
                self.Modulo = "%"
                self.Bitwise_And = "&"
                self.Bitwise_Or = "|"
                self.Bitwise_Xor  = "^"
                self.Bitwise_Not  = "~"
                self.Bitshift_Right = ">>"
                self.Bitshift_Left = "<<"
                self.And = "&&"
                self.Or = "||"
                self.Not_Equal = "!="
                self.Double_Equal = "=="
                self.Not = "!"
                self.Less = "<"
                self.Less_Equal = "<="
                self.Greater = ">"
                self.Greater_Equal = ">="
                self.Equal = "="
            def __repr__(self) -> str:
                return str(vars(self))
        self.Operators = _Operators()

        class _Closures():
            def __init__(self) -> None:
                self.Paren_Open = "("
                self.Paren_Close = ")"
                self.Square_Open = "["
                self.Square_Close = "]"
                self.Curly_Open = "{"
                self.Curly_Close = "}"
            def __repr__(self) -> str:
                return str(vars(self))
            def get_all(self):
                return [self.Paren_Open, self.Paren_Close, self.Curly_Close, self.Curly_Open]
            def get_close(self):
                return [self.Paren_Close, self.Curly_Close]
            def get_open(self):
                return [self.Paren_Open, self.Curly_Open]
        self.Closures = _Closures()

        class _Keywords():
            def __init__(self) -> None:
                self.If = "if"
                self.Else = "else"
                self.While = "while"
            def __repr__(self) -> str:
                return str(vars(self))
        self.Keywords = _Keywords()

        class _Functions():
            def __init__(self) -> None:
                self.Log = "log"
                self.Print = "print"
                self.To_Int = "to_int"
                self.To_Float = "to_float"
                self.To_Bool = "to_bool"
                self.To_String = "to_string"
            def __repr__(self) -> str:
                return str(vars(self))
        self.Functions = _Functions()

        class _Literals():
            def __init__(self) -> None:
                self.Int = "int"
                self.Float = "float"
                self.Bool = "bool"
                self.String = 'string'
            def __repr__(self) -> str:
                return str(vars(self))
        self.Literals = _Literals()

        class _Identifiers():
            def __init__(self) -> None:
                self.Iden = "iden"
            def __repr__(self) -> str:
                return str(vars(self))
        self.Identifiers = _Identifiers()
        
        class _Comments():
            def __init__(self) -> None:
                self.Comment = "#"
                self.Block_Comment_Open = '/*'
                self.Block_Comment_Close = '*/'
            def __repr__(self) -> str:
                return str(vars(self))
        self.Comments = _Comments()

        class _Line_End():
            def __init__(self) -> None:
                self.Line_End = ";"
            def __repr__(self) -> str:
                return str(vars(self))
        self.Line_End = _Line_End()

    def __repr__(self) -> str:
        return str(vars(self))
Token_Enum = _Token_Enum()


### ======================================== Lexemes / Errors ======================================== ###


class Lexeme_Implementation_Error(BaseException):
    """Exception raised because the base Lexeme Class was improperly used

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, message: str) -> None:
        self.message = message


### ======================================== Lexemes ======================================== ###

class _Lexeme_State_Enum():
    def __init__(self) -> None:
        self.failed = "failed"
        self.open = "open"
        self.accept = "accept" # implies open and complete
        self.complete = "complete"

    def __repr__(self) -> str:
        return str(vars(self))
Lexeme_State_Enum = _Lexeme_State_Enum()


class Lexeme():

    def __init__(self) -> None:
        self.reset()
        self._token = None

    ### Setters
    def reset(self) -> None:
        self._captured = []
        self._state = Lexeme_State_Enum.open
        self._mode = 0

    def set_fail(self) -> None:
        self._state = Lexeme_State_Enum.failed

    def set_complete(self) -> None:
        self._state = Lexeme_State_Enum.complete

    def set_accept(self) -> None:
        self._state = Lexeme_State_Enum.accept
    
    def feed(self, char: str) -> int:
        raise(Lexeme_Implementation_Error("Lexeme base class feed method called"))
        return self._state

    ### Getters
    def is_open(self) -> bool:
        return self._state == Lexeme_State_Enum.open or self._state == Lexeme_State_Enum.accept

    def is_failed(self) -> bool:
        return self._state == Lexeme_State_Enum.failed

    def is_complete(self) -> bool:
        return self._state == Lexeme_State_Enum.complete or self._state == Lexeme_State_Enum.accept

    def get_state(self) -> int:
        return self._state

    def get_captured(self) -> str:
        return "".join(self._captured)

    def get_token(self) -> str:
        return self._token


class Lexeme_Multi_Char(Lexeme):

    def __init__(self, token, *chars) -> None:
        super().__init__()
        self._token = token
        self._chars = chars
    
    def feed(self, char: str) -> int:
        if not self.is_open():
            return self._state
            
        if self._mode in range(len(self._chars)):
            if char == self._chars[self._mode]:
                self._captured.append(char)
                if self._mode == len(self._chars)-1:
                    self.set_complete()
                self._mode += 1
            else:
                self.set_fail()
        else:
            print('unknown mode')

        return self._state


### ======================================== Lexemes / Operators - Double ======================================== ###


# self.Power = "**"
class Lxm_Op_Power(Lexeme_Multi_Char):

    def __init__(self) -> None:
        super().__init__(Token_Enum.Operators.Power, '*', '*')


# self.Int_Division = "//"
class Lxm_Op_Int_Division(Lexeme_Multi_Char):

    def __init__(self) -> None:
        super().__init__(Token_Enum.Operators.Int_Division, '/', '/')


# self.Bitshift_Right = ">>"
class Lxm_Op_Bitshift_Right(Lexeme_Multi_Char):

    def __init__(self) -> None:
        super().__init__(Token_Enum.Operators.Bitshift_Right, '>', '>')


# self.Bitshift_Left = "<<"
class Lxm_Op_Bitshift_Left(Lexeme_Multi_Char):

    def __init__(self) -> None:
        super().__init__(Token_Enum.Operators.Bitshift_Left, '<', '<')


# self.And = "&&"
class Lxm_Op_And(Lexeme_Multi_Char):

    def __init__(self) -> None:
        super().__init__(Token_Enum.Operators.And, '&', '&')


# self.Or = "||"
class Lxm_Op_Or(Lexeme_Multi_Char):

    def __init__(self) -> None:
        super().__init__(Token_Enum.Operators.Or, '|', '|')


# self.Not_Equal = "!="
class Lxm_Op_Not_Equal(Lexeme_Multi_Char):

    def __init__(self) -> None:
        super().__init__(Token_Enum.Operators.Not_Equal, '!', '=')


# self.Double_Equal = "=="
class Lxm_Op_Double_Equal(Lexeme_Multi_Char):

    def __init__(self) -> None:
        super().__init__(Token_Enum.Operators.Double_Equal, '=', '=')


# self.Less_Equal = "<="
class Lxm_Op_Less_Equal(Lexeme_Multi_Char):

    def __init__(self) -> None:
        super().__init__(Token_Enum.Operators.Less_Equal, '<', '=')


# self.Greater_Equal = ">="
class Lxm_Op_Greater_Equal(Lexeme_Multi_Char):

    def __init__(self) -> None:
        super().__init__(Token_Enum.Operators.Greater_Equal, '>', '=')


### ======================================== Lexemes / Operators - Single ======================================== ###


# self.Add = "+"
class Lxm_Op_Add(Lexeme_Multi_Char):

    def __init__(self) -> None:
        super().__init__(Token_Enum.Operators.Add, '+')


# self.Subtract = "-"
class Lxm_Op_Subtract(Lexeme_Multi_Char):

    def __init__(self) -> None:
        super().__init__(Token_Enum.Operators.Subtract, '-')


# self.Multiply = "*"
class Lxm_Op_Multiply(Lexeme_Multi_Char):

    def __init__(self) -> None:
        super().__init__(Token_Enum.Operators.Multiply, '*')


# self.Division = "/"
class Lxm_Op_Division(Lexeme_Multi_Char):

    def __init__(self) -> None:
        super().__init__(Token_Enum.Operators.Division, '/')


# self.Modulo = "%"
class Lxm_Op_Modulo(Lexeme_Multi_Char):

    def __init__(self) -> None:
        super().__init__(Token_Enum.Operators.Modulo, '%')


# self.Bitwise_And = "&"
class Lxm_Op_Bitwise_And(Lexeme_Multi_Char):

    def __init__(self) -> None:
        super().__init__(Token_Enum.Operators.Bitwise_And, '&')


# self.Bitwise_Or = "|"
class Lxm_Op_Bitwise_Or(Lexeme_Multi_Char):

    def __init__(self) -> None:
        super().__init__(Token_Enum.Operators.Bitwise_Or, '|')


# self.Bitwise_Xor  = "^"
class Lxm_Op_Bitwise_Xor(Lexeme_Multi_Char):

    def __init__(self) -> None:
        super().__init__(Token_Enum.Operators.Bitwise_Xor, '^')


# self.Bitwise_Not  = "~"
class Lxm_Op_Bitwise_Not(Lexeme_Multi_Char):

    def __init__(self) -> None:
        super().__init__(Token_Enum.Operators.Bitwise_Not, '~')


# self.Not = "!"
class Lxm_Op_Not(Lexeme_Multi_Char):

    def __init__(self) -> None:
        super().__init__(Token_Enum.Operators.Not, '!')


# self.Less = "<"
class Lxm_Op_Less(Lexeme_Multi_Char):

    def __init__(self) -> None:
        super().__init__(Token_Enum.Operators.Less, '<')


# self.Greater = ">"
class Lxm_Op_Greater(Lexeme_Multi_Char):

    def __init__(self) -> None:
        super().__init__(Token_Enum.Operators.Greater, '>')


# self.Equal = "="
class Lxm_Op_Equal(Lexeme_Multi_Char):

    def __init__(self) -> None:
        super().__init__(Token_Enum.Operators.Equal, '=')


### ======================================== Lexemes / Closures ======================================== ###


# self.Paren_Open = "("
class Lxm_Close_Paren_Open(Lexeme_Multi_Char):

    def __init__(self) -> None:
        super().__init__(Token_Enum.Closures.Paren_Open, '(')


# self.Paren_Close = ")"
class Lxm_Close_Paren_Close(Lexeme_Multi_Char):

    def __init__(self) -> None:
        super().__init__(Token_Enum.Closures.Paren_Close, ')')

        
# self.Square_Open = "["
class Lxm_Close_Square_Open(Lexeme_Multi_Char):

    def __init__(self) -> None:
        super().__init__(Token_Enum.Closures.Square_Open, '[')

        
# self.Square_Close = "]"
class Lxm_Close_Square_Close(Lexeme_Multi_Char):

    def __init__(self) -> None:
        super().__init__(Token_Enum.Closures.Square_Close, ']')

        
# self.Curly_Open = "{"
class Lxm_Close_Curly_Open(Lexeme_Multi_Char):

    def __init__(self) -> None:
        super().__init__(Token_Enum.Closures.Curly_Open, '{')

        
# self.Curly_Close = "}"
class Lxm_Close_Curly_Close(Lexeme_Multi_Char):

    def __init__(self) -> None:
        super().__init__(Token_Enum.Closures.Curly_Close, '}')

        
### ======================================== Lexemes / Keywords ======================================== ###


# self.If = "if"
class Lxm_Keywords_If(Lexeme_Multi_Char):

    def __init__(self) -> None:
        super().__init__(Token_Enum.Keywords.If, *list("if"))


# self.Else = "else"
class Lxm_Keywords_Else(Lexeme_Multi_Char):

    def __init__(self) -> None:
        super().__init__(Token_Enum.Keywords.Else, *list("else"))


# self.While = "while"
class Lxm_Keywords_While(Lexeme_Multi_Char):

    def __init__(self) -> None:
        super().__init__(Token_Enum.Keywords.While, *list("while"))


### ======================================== Lexemes / Functions ======================================== ###


# self.Log = "log"
class Lxm_Function_Log(Lexeme_Multi_Char):

    def __init__(self) -> None:
        super().__init__(Token_Enum.Functions.Log, *list("log"))


# self.Print = "print"
class Lxm_Function_Print(Lexeme_Multi_Char):

    def __init__(self) -> None:
        super().__init__(Token_Enum.Functions.Print, *list("print"))


# self.To_Int = "to_int"
class Lxm_Function_To_Int(Lexeme_Multi_Char):

    def __init__(self) -> None:
        super().__init__(Token_Enum.Functions.To_Int, *list("to_int"))


# self.To_Float = "to_float"
class Lxm_Function_To_Float(Lexeme_Multi_Char):

    def __init__(self) -> None:
        super().__init__(Token_Enum.Functions.To_Float, *list("to_float"))

# self.To_Bool = "to_bool"
class Lxm_Function_To_Bool(Lexeme_Multi_Char):

    def __init__(self) -> None:
        super().__init__(Token_Enum.Functions.To_Bool, *list("to_bool"))


# self.To_String = "to_string"
class Lxm_Function_To_String(Lexeme_Multi_Char):

    def __init__(self) -> None:
        super().__init__(Token_Enum.Functions.To_String, *list("to_string"))


### ======================================== Lexemes / Literals ======================================== ###


# self.Int = "int"
class Lxm_Literals_Int(Lexeme):
    """
        Integers contain only numbers [0-9]
        All Integers can start with a minus sign
    """
    def __init__(self) -> None:
        super().__init__()
        self._token = Token_Enum.Literals.Int
        
    
    def feed(self, char: str) -> int:
        if not self.is_open():
            return self._state
            
        ### Complete feed function
        if self._mode == 0:
            if char == "-" and len(self._captured) == 0:
                self._captured.append(char)
            elif re.match(r'[0-9]', char):
                self._mode = 1
                self._captured.append(char)
                self.set_accept()
            else:
                self.set_fail()
        elif self._mode == 1:
            if re.match(r'[0-9]', char):
                self._captured.append(char)
            else:
                self.set_complete()

        return self._state


# self.Float = "float"
class Lxm_Literals_Float(Lexeme):
    """
        Floating points consist of one of the following:
            A decimal point followed by one or more numbers [0-9]
            One or more numbers followed by a decimal point
            Numbers, a decimal point, followed by more numbers
        All floating points can start with a minus sign
    """
    def __init__(self) -> None:
        super().__init__()
        self._token = Token_Enum.Literals.Float
        
    
    def feed(self, char: str) -> int:
        if not self.is_open():
            return self._state
        
        ### Complete feed function
        if self._mode == 0:
            if char == "-" and len(self._captured) == 0:
                self._captured.append(char)
            elif re.match(r'[0-9]', char) != None:
                self._mode = 1
                self._captured.append(char)
            elif char == ".":
                self._mode = 2
                self._captured.append(char)
            else:
                self.set_fail()
        elif self._mode == 1:
            if char == ".":
                self._mode = 2
                self._captured.append(char)
                self.set_accept()
            elif re.match(r'[0-9]', char) != None:
                self._captured.append(char)
            else:
                self.set_fail()
        elif self._mode == 2:
            if re.match(r'[0-9]', char) != None:
                self._captured.append(char)
                self.set_accept()
            elif self._state == Lexeme_State_Enum.accept:
                self.set_complete()
            else:
                self.set_fail()
        else:
            self.set_fail()

        return self._state


# self.Bool = "bool"
class Lxm_Literals_Bool(Lexeme):
    """
        Valid booleans are either True or False
    """
    def __init__(self) -> None:
        super().__init__()
        self._token = Token_Enum.Literals.Bool
        self._mode2 = 0
        self._False = list("False")
        self._True = list("True")
        
    
    def feed(self, char: str) -> int:
        if not self.is_open():
            return self._state
            
        ### Complete feed function
        '''
        if char == self._False[self._mode]:
            self._mode += 1
            self._captured.append(char)
        if char == self._True[self._mode2]:
        '''
        if self._mode in range(len(self._False)):
            if char == self._False[self._mode]:
                self._captured.append(char)
                if self._mode == len(self._False)-1:
                    self.set_complete()
                self._mode += 1
            elif char == self._True[self._mode]:
                self._captured.append(char)
                if self._mode == len(self._True)-1:
                    self.set_complete()
                self._mode += 1
            else:
                self.set_fail()

        return self._state


# self.String = '"*"'
class Lxm_Literals_String(Lexeme):
    """
        Strings start with a quotation mark and contain all characters precieding the next quotation mark
        Capture only the characters between the quotation marks.
    """
    def __init__(self) -> None:
        super().__init__()
        self._token = Token_Enum.Literals.String
        
    
    def feed(self, char: str) -> int:
        if not self.is_open():
            return self._state
            
        ### Complete feed function
        if self._mode == 0 and char == '"':
            self._captured.append(char)
            self._mode += 1
        elif self._mode != 0 and char != '"':
            self._captured.append(char)
            self._mode += 1
        elif char == '"':
            self._captured.append(char)
            self._mode += 1
            self.set_complete()
        else:
            self.set_fail()


        return self._state


### ======================================== Lexemes / Identifiers ======================================== ###


# self.Iden = 'iden'
class Lxm_Identifiers_Iden(Lexeme):
    """
        Identifiers start with an underscore or a letter [A-Za-z_],
        they may then contain any number of underscores, letters, and numbers [A-Za-z0-9_]
    """
    
    def __init__(self) -> None:
        super().__init__()
        self._token = Token_Enum.Identifiers.Iden
        
    
    def feed(self, char: str) -> int:
        if not self.is_open():
            return self._state
            
        ### Complete feed function
        if self._mode == 0 and re.match(r'[A-Za-z_]', char) != None:
            self._captured.append(char)
            self._mode = 1
            self.set_accept()
        elif re.match(r'[A-Za-z0-9_]', char) != None and self._mode != 0:
            self._captured.append(char)
        elif len(self._captured) > 0 and self._mode != 0:
            self.set_complete()
        else:
            self.set_fail()

        return self._state


### ======================================== Lexemes / Comments ======================================== ###


# self.Comment = "comment"
class Lxm_Comment_Single(Lexeme):
    """
        Strings start with a quotation mark and contain all characters precieding the next quotation mark
        Capture only the characters between the quotation marks.
    """
    def __init__(self) -> None:
        super().__init__()
        self._token = Token_Enum.Comments.Comment
        
    
    def feed(self, char: str) -> int:
        if not self.is_open():
            return self._state
            
        ### Complete feed function
        if self._mode == 0:
            if char == '#':
                self._captured.append(char)
                self.set_accept()
                self._mode = 1
            else:
                self.set_fail()

        elif self._mode == 1:
            if char != '\n':
                self._captured.append(char)
            else:
                self.set_complete()

        # print(char, self._captured, self._state)
                
        return self._state


class Lxm_Comment_Block(Lexeme):
    """
        Strings start with a quotation mark and contain all characters precieding the next quotation mark
        Capture only the characters between the quotation marks.
    """
    def __init__(self) -> None:
        super().__init__()
        self._token = Token_Enum.Comments.Comment
        
    
    def feed(self, char: str) -> int:
        if not self.is_open():
            return self._state
            
        ### Complete feed function
        if self._mode == 0:
            if char == '/':
                self._captured.append(char)
                self._mode = 1
            else:
                self.set_fail()

        elif self._mode == 1:
            if char == '*':
                self._captured.append(char)
                self._mode = 2
            else:
                self.set_fail()

        elif self._mode == 2:
            self._captured.append(char)
            if char == '*':
                self._mode = 3

        elif self._mode == 3:
            self._captured.append(char)
            if char == '/':
                self.set_complete()
            else:
                self._mode = 2

        return self._state

### ======================================== Lexemes / Line_End ======================================== ###


# self.Line_End = ";"
class Lxm_Line_End(Lexeme_Multi_Char):

    def __init__(self) -> None:
        super().__init__(Token_Enum.Line_End.Line_End, ';')