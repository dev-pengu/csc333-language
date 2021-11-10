from Lexer.Token import Token
from Lexer.Lexemes.Lexemes import Token_Enum
from typing import List
from AST.AST_Nodes import *
from copy import deepcopy
from Parser.Parser_Syntax_Error import Parser_Syntax_Error
from stubs.AST_Statement_Stub import AST_Statement_Stub

### ==================================== Private Functions ==================================== ###
CLOSURE_TYPES = [
    Token_Enum.Closures.Paren_Close,
    Token_Enum.Closures.Paren_Open,
    Token_Enum.Closures.Curly_Open,
    Token_Enum.Closures.Curly_Close,
]

def find_closure_tokens(tokens: List[Token]) -> List[Token]:
    if tokens[0].get_type() not in [Token_Enum.Closures.Paren_Open, Token_Enum.Closures.Curly_Open]:
        raise(Parser_Syntax_Error('Function find_closure_tokens given stream beginning with {}'.format(tokens[0])))
    closure_tokens =[tokens.pop(0)]
    closure_stack = [closure_tokens[0].get_type()]

    while tokens:
        next_token = tokens.pop(0)
        closure_tokens.append(next_token)
        token_type = next_token.get_type()

        if token_type not in CLOSURE_TYPES:
            continue
        if token_type in [Token_Enum.Closures.Curly_Open, Token_Enum.Closures.Paren_Open]:
            closure_stack.append(token_type)
        else:
            closure_stack.pop()
        
        if not closure_stack:
            break
    if not closure_stack:
        raise Parser_Syntax_Error('Reached EOF before matching closure could be found')
    
    return closure_tokens

def find_next_statement(tokens:List[Token]) -> List[Token]:
    
    statement_tokens = []
    closure_stack = []

    while tokens:
        next_token = tokens.pop(0)
        statement_tokens.append(next_token)
        token_type = next_token.get_type()

        if len(closure_stack) == 0 and token_type == Token_Enum.Line_End.Line_End:
            break

        ### check if the token is relevant, if not continue
        if token_type not in CLOSURE_TYPES+[Token_Enum.Line_End.Line_End]:
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

### ========================================================================================== ###

### ==================================== Forward Casting ===================================== ###
def Parse_Expression(tokens: List[Token]) -> AST_Node:
    pass
def Parse_Statement(tokens: List[Token]) -> AST_Node:
    pass
def Parse_Blocks(tokens: List[Token]) -> AST_Node:
    pass

### ========================================================================================== ###

### ==================================== Public Functions ==================================== ###

def Parse_Expression(tokens: List[Token]) -> AST_Node:
    return AST_Expression_Stub() # TODO: implement AST_Expression_Stub

def Parse_Statement(tokens:List[Token]) -> AST_Node:

    if tokens[-1].get_type() != Token_Enum.Line_End.Line_End:
        raise(Parser_Syntax_Error('Reached EOF while parsing statement, expected ;'))
    
    statement_node = None

    if tokens[0].get_type() == Token_Enum.Keywords.While:
        statement_node = AST_Statement_While() #TODO: implement AST_Statement_While
        tokens.pop(0)
        if tokens[0].get_type() == Token_Enum.Closures.Paren_Open:
            raise(Parser_Syntax_Error('Expected ( following loop definition'))
        closure_tokens = find_closure_tokens(tokens)
        condition = Parse_Expression(closure_tokens)



def Parse_Blocks(tokens:List[Token]) -> AST_Node:
    tokens = deepcopy(tokens)
    
    stack = []
    root = None # root node to be returned
    
    while tokens:
        next_statement_tokens = find_next_statement(tokens)
        next_statement_node = Parse_Statement(next_statement_tokens)
        
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

### ===========================================================================================  ###
