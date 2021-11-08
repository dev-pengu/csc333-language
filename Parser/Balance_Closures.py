from Lexer.Lexer import *
from Lexer.Lexemes.Lexemes import *
from Lexer.Token import Token
from typing import List
import copy
import Parser_Syntax_Error

def Balance_Closures(tokens:List[Token]) -> None:
    tokens = copy.deepcopy(tokens)

    closure_types = [
        Token_Enum.Closures.Paren_Close,
        Token_Enum.Closures.Paren_Open,
        Token_Enum.Closures.Curly_Open,
        Token_Enum.Closures.Curly_Close,
    ]

    closure_stack = []

    while tokens:
        next_token = tokens.pop(0)

        token_type = next_token.get_type()

        ### check if the token is relevant, if not continue
        if token_type not in closure_types+[Token_Enum.Line_End.Line_End]:
            continue

        if closure_stack: # the stack is not empty
            stack_type = closure_stack[-1]

            ### Error conditions
            if stack_type == Token_Enum.Closures.Paren_Open and \
                    token_type == Token_Enum.Closures.Curly_Close:
                raise(Parser_Syntax_Error("( cannot match with }"))

            if stack_type == Token_Enum.Closures.Curly_Open and \
                    token_type == Token_Enum.Closures.Paren_Close:
                raise(Parser_Syntax_Error("{ cannot match with )"))

            if stack_type == Token_Enum.Closures.Paren_Open:
                if token_type == Token_Enum.Line_End.Line_End:
                    raise(Parser_Syntax_Error("LineEnd found before matching )"))

                if token_type == Token_Enum.Closures.Curly_Open:
                    raise(Parser_Syntax_Error("Found { following unclosed (\n\tStatements cannot be included inside expressions"))

            ### Matching closure conditions
            if token_type == Token_Enum.Closures.Paren_Close or \
                        token_type == Token_Enum.Closures.Curly_Close:
                closure_stack.pop()
            else:
                if token_type != Token_Enum.Line_End.Line_End:
                    closure_stack.append(token_type)

        else: # the stack is empty
            if token_type in [Token_Enum.Closures.Paren_Close,
                                        Token_Enum.Closures.Curly_Close]:
                raise(Parser_Syntax_Error("Found {} with no matching open token".format(token_type)))
            elif token_type != Token_Enum.Line_End.Line_End:
                closure_stack.append(token_type)
    
    if closure_stack:
        raise(Parser_Syntax_Error("Found the following unmatched closures {}".format(closure_stack)))
