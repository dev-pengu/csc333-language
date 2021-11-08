from Lexer.Lexemes.Lexemes import *
from Lexer.Token import Token
from typing import List


### ======================================== Lexer / Errors ======================================== ###


class Lexer_Match_Error(BaseException):
    """Exception raised because the base Lexer could not find a matching token

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message: str) -> None:
        self.message = message


### ======================================== Lexer ======================================== ###

class Lexer():

    def __init__(self) -> None:
        self._lexemes = [
            Lxm_Op_Power,Lxm_Op_Int_Division,Lxm_Op_Bitshift_Right,Lxm_Op_Bitshift_Left,Lxm_Op_And,Lxm_Op_Or,Lxm_Op_Not_Equal,Lxm_Op_Double_Equal,Lxm_Op_Less_Equal,Lxm_Op_Greater_Equal,
            Lxm_Op_Add,Lxm_Op_Subtract,Lxm_Op_Multiply,Lxm_Op_Division,Lxm_Op_Modulo,Lxm_Op_Bitwise_And,Lxm_Op_Bitwise_Or,Lxm_Op_Bitwise_Xor,Lxm_Op_Bitwise_Not,Lxm_Op_Not,Lxm_Op_Less,Lxm_Op_Greater,Lxm_Op_Equal,
            Lxm_Close_Paren_Open,Lxm_Close_Paren_Close,Lxm_Close_Square_Open,Lxm_Close_Square_Close,Lxm_Close_Curly_Open,Lxm_Close_Curly_Close,
            Lxm_Keywords_If,Lxm_Keywords_Else,Lxm_Keywords_While,
            Lxm_Function_Log,Lxm_Function_Print,Lxm_Function_To_Int,Lxm_Function_To_Float,Lxm_Function_To_Bool,Lxm_Function_To_String,
            Lxm_Line_End,
            Lxm_Literals_Int, Lxm_Literals_Float, Lxm_Literals_Bool, Lxm_Literals_String,
            Lxm_Identifiers_Iden,
            Lxm_Comment_Single, Lxm_Comment_Block,
        ]
        self._lexemes = [l() for l in self._lexemes]


    def _possible_tokens(self, char_stream:List[str]) -> List[Token]:
        char_stream = char_stream.copy()
        [lxm.reset() for lxm in self._lexemes]

        ### feed the char_stream to the lexemes one character at a time
        ### Important! do not modify the character stream
        ### TODO: write this code
        any_open = True
        i = 0
        while i < len(char_stream) and any_open:
            any_open = False
            for lxm in self._lexemes:
                lxm.feed(char_stream[i])
                if lxm.is_open():
                    any_open = True
            i+= 1

        possible_tokens = []
        ### fill the list with tokens that match the head of the char_stream
        ### TODO: write this code
        for lxm in self._lexemes:
            if lxm.is_complete():
                possible_tokens.append(Token(lxm.get_token(), lxm.get_captured()))

        ### return the list of tokens
        return possible_tokens
        

    def match_tokens(self, char_stream:str) -> List[str]:

        tokens = []
        
        char_stream = list(char_stream)
        
        while len(char_stream) > 0:
            ### skip any leading whitespace
            ### TODO: write this code
            while(len(char_stream) > 0 and char_stream[0].isspace()):
                char_stream.pop(0)
                
            if (len(char_stream) == 0):
                break

            ### get the possible token matches to the char_stream
            possible_tokens = self._possible_tokens(char_stream)

            ### make sure at least one token matched and raise an error if none did
            if len(possible_tokens) == 0:
                raise(Lexer_Match_Error("No matching Token for:\n{}".format(''.join(char_stream))))

            ### otherwise resolve any conflicts and append the token to tokens
            ### TODO: write this code
            token = possible_tokens[0]
            for i in range(1, len(possible_tokens)):
                if (len(possible_tokens[i].get_string()) > len(token.get_string())) or \
                    (len(possible_tokens[i].get_string()) == len(token.get_string()) and token.get_type() == Token_Enum.Identifiers.Iden):
                    token = possible_tokens[i]
            tokens.append(token)

            ### remove the captured characters from the front of the character_stream
            new_token = tokens[-1]
            char_stream = char_stream[len(new_token.get_string()):]

            ### remove the parenthesis from any strings
            if new_token.get_type() == Token_Enum.Literals.String:
                new_token.set_string(new_token.get_string()[1:-1])

        return tokens
                    



                    


                



            
        


