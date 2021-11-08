from Lexer.Token import Token
from Lexer.Lexemes.Lexemes import Token_Enum
from typing import List
from AST.AST_Nodes import *
from copy import deepcopy
from Parser.Parser_Syntax_Error import Parser_Syntax_Error
from Parser.Parse_Statement import Parse_Statement

def find_next_statement(tokens:List[Token]) -> AST_Node:
    
    statement_tokens = []
    closure_types = [
        Token_Enum.Closures.Paren_Close,
        Token_Enum.Closures.Paren_Open,
        Token_Enum.Closures.Curly_Open,
        Token_Enum.Closures.Curly_Close,
    ]
    closure_stack = []

    while tokens:
        next_token = tokens.pop(0)
        statement_tokens.append(next_token)
        token_type = next_token.get_type()

        if len(closure_stack) == 0 and token_type == Token_Enum.Line_End.Line_End:
            break

        ### check if the token is relevant, if not continue
        if token_type not in closure_types+[Token_Enum.Line_End.Line_End]:
            continue

        if closure_stack: # the stack is not empty
            ### Matching closure conditions
            if token_type == Token_Enum.Closures.Paren_Close or \
                        token_type == Token_Enum.Closures.Curly_Close:
                closure_stack.pop()
            else:
                if token_type != Token_Enum.Line_End.Line_End:
                    closure_stack.append(token_type)
        else: # the stack is empty
            if token_type in [Token_Enum.Closures.Paren_Open,
                                        Token_Enum.Closures.Curly_Open]:
                closure_stack.append(token_type)
    
    return statement_tokens


def Parse_Blocks(tokens:List[Token]) -> AST_Node:
    tokens = deepcopy(tokens)
    
    stack = []
    root = None # root node to be returned
    
    id = 1
    while tokens:
        next_statement_tokens = find_next_statement(tokens)
        next_statement_node = Parse_Statement(next_statement_tokens, id)
        id += 1
        
        #print(next_statement_tokens, '\n')

        stack.append(next_statement_node)
    
    last_block_list = None
    next_block_list = None
    while stack:
        next_statement_node = stack.pop()
        if next_block_list:
            last_block_list = next_block_list
        else:
            last_block_list = AST_Block_List()
            if len(stack) == 0:
                root = next_statement_node
            else:
                root = last_block_list
        if len(stack) > 1:
            next_block_list = AST_Block_List()
            last_block_list.affix_nodes(next_block_list, next_statement_node)
        else:
            last_block_list.affix_nodes(stack.pop(), next_statement_node)



    return root