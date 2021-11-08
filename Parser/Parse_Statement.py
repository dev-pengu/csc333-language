from Lexer.Token import Token
from Lexer.Lexemes.Lexemes import Token_Enum
from typing import List
from AST.AST_Nodes import *
from stubs.AST_Statement_Stub import AST_Statement_Stub
from copy import deepcopy
from Parser.Parser_Syntax_Error import Parser_Syntax_Error


def Parse_Statement(tokens:List[Token], id: int) -> AST_Node:
    '''TODO: Temp code below. (needs to be removed)'''
    tokens = deepcopy(tokens)

    if tokens[-1].get_type() != Token_Enum.Line_End.Line_End:
        raise(Parser_Syntax_Error('Reached EOF while parsing statement, expected ;'))
    
    return AST_Statement_Stub(id)
    