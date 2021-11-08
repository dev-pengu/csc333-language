import time
import random
import math



### ======================================== Tools ======================================== ###



### ======================================== Errors ======================================== ###


class AST_Build_Error(BaseException):
    """Exception raised for errors during the AST building process.

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, message: str) -> None:
        self.message = message


class AST_Runtime_Error(BaseException):
    """Exception raised for errors during the AST building process.

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, message: str) -> None:
        self.message = message


### ======================================== Base Classes ======================================== ###


class _Type_Enum():
    def __init__(self) -> None:
        self.undefined = 0
        self.int = 1
        self.float = 2
        self.bool = 3
        self.str = 4

    def __repr__(self) -> str:
        return str(vars(self))
Type_Enum = _Type_Enum()


class AST_Data():
    """

    """

    def __init__(self):
        self._value = None
        self._type = Type_Enum.undefined

    def get_value(self):
        return self._value

    def set_value(self, new_value) -> None:
        self._value = new_value

    def get_type(self) -> int:
        return self._type

    def set_type(self, new_type: int) -> None:
        self._type = new_type

    def __repr__(self) -> str:
        return str(vars(self))


class AST_Variable(AST_Data):
    """

    """

    def __init__(self, name = "", data: AST_Data = None):
        super().__init__()
        self._name = name
        if data != None:
            self.set_type(data.get_type())
            self.set_value(data.get_value())

    def get_name(self):
        return self._name

    def set_name(self, name) -> None:
        self._name = name


class Name_Space():
    """

    """

    def __init__(self):
        self._name_space = {}

    def get(self, name) -> AST_Variable:
        if name not in self._name_space:
            return AST_Variable(name)
        return self._name_space[name]

    def set(self, name: str, new_data: AST_Data) -> None:
        var = AST_Variable(name, new_data)
        self._name_space[name] = var


class Abstract_Syntax_Tree():
    """

    """

    def __init__(self, root) -> None:
        self._root = root

    def walk(self) -> AST_Data:
        name_space = Name_Space()
        return self._root.walk(name_space), name_space


class AST_Node():
    """

    """

    def __init__(self) -> None:
        self._affixed_nodes = []
        self._expected_nodes = []

    def affix_nodes(self) -> None:
        pass

    def verify_node(self) -> None:
        if len(self._affixed_nodes) != len(self._expected_nodes):
            raise AST_Build_Error("{}: Wrong number of affixed nodes. Expected {}, got {}".format(type(self), len(self._expected_nodes), len(self._affixed_nodes)))
        if False in [isinstance(a,b) for a,b in zip(self._affixed_nodes, self._expected_nodes)]:
            raise AST_Build_Error("{}: Wrong types of affixed nodes. Expected {}, got {}".format(type(self), self._expected_nodes, [type(a) for a in self._affixed_nodes]))

    def walk(self, name_space: Name_Space) -> AST_Data:
        return AST_Data()


### !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! Forward_Declarations !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! ###


class AST_Block_List(AST_Node):
    pass
class AST_Statement(AST_Block_List):
    pass
class AST_Expression(AST_Statement):
    pass
class AST_Literal(AST_Expression):
    pass
class AST_Identifier(AST_Expression):
    pass

### ======================================== Block_List ======================================== ###


class AST_Block_List(AST_Node):
    """

    """

    def __init__(self) -> None:
        super(AST_Node, self).__init__()
        self._expected_nodes = [AST_Block_List, AST_Statement]

    def affix_nodes(self, block_list_top: AST_Block_List, statement_bot: AST_Statement) -> None:
        self._affixed_nodes = [block_list_top, statement_bot]
        self.verify_node()

    def walk(self, name_space: Name_Space) -> AST_Data:
        
        self._affixed_nodes[0].walk(name_space)
        self._affixed_nodes[1].walk(name_space)

        return AST_Data()


### ======================================== Block_List / Statement ======================================== ###


class AST_Statement(AST_Block_List):
    """

    """

    def __init__(self) -> None:
        super(AST_Node, self).__init__()

    def affix_nodes(self) -> None:
        pass

    def walk(self, name_space: Name_Space) -> AST_Data:
        self.verify_node()
        return AST_Data()


class AST_Statement_Assignment(AST_Statement):
    """

    """

    def __init__(self) -> None:
        super(AST_Node, self).__init__()
        self._expected_nodes = [AST_Identifier, AST_Expression]

    def affix_nodes(self, identifier_lhs: AST_Identifier, expression_rhs: AST_Expression) -> None:
        self._affixed_nodes = [identifier_lhs, expression_rhs]
        self.verify_node()

    def walk(self, name_space: Name_Space) -> AST_Data:
        
        var_lhs = self._affixed_nodes[0].walk(name_space)
        data_rhs = self._affixed_nodes[1].walk(name_space)

        if data_rhs.get_type() == Type_Enum.undefined:
            raise AST_Runtime_Error("{}: Right hand expression is undefined".format(type(self)))

        if var_lhs.get_type() == Type_Enum.undefined:
            name_space.set(var_lhs.get_name(), data_rhs)
        else:
            var_lhs.set_value(data_rhs.get_value())
            var_lhs.set_type(data_rhs.get_type())
        
        return AST_Data()


### ======================================== Block_List / Statement / Expression ======================================== ###


class AST_Expression(AST_Statement):
    """

    """

    def __init__(self) -> None:
        super(AST_Node, self).__init__()

    def affix_nodes(self) -> None:
        pass

    def walk(self, name_space: Name_Space) -> AST_Data:
        return AST_Data()


class AST_Expression_Addition(AST_Expression):
    """

    """

    def __init__(self) -> None:
        super(AST_Node, self).__init__()
        self._expected_nodes = [AST_Expression, AST_Expression]

    def affix_nodes(self, expression_lhs: AST_Expression, expression_rhs: AST_Expression) -> None:
        self._affixed_nodes = [expression_lhs, expression_rhs]
        self.verify_node()

    def walk(self, name_space: Name_Space) -> AST_Data:
        node_ret = AST_Data()
        
        data_lhs = self._affixed_nodes[0].walk(name_space)
        data_rhs = self._affixed_nodes[1].walk(name_space)

        if (data_lhs.get_type() in (Type_Enum.int, Type_Enum.float, Type_Enum.bool) and # Add numbers
                data_rhs.get_type() in (Type_Enum.int, Type_Enum.float, Type_Enum.bool)):
            node_ret.set_value(data_lhs.get_value() + data_rhs.get_value())

            if (data_lhs.get_type() == Type_Enum.float or # Check for floating-point
                    data_rhs.get_type() == Type_Enum.float):
                node_ret.set_type(Type_Enum.float)
            else:
                node_ret.set_type(Type_Enum.int)

        elif (data_lhs.get_type() == Type_Enum.str and # Concatenate strings
                data_rhs.get_type() == Type_Enum.str):
            node_ret.set_value(data_lhs.get_value() + data_rhs.get_value())
            node_ret.set_type()

        elif data_lhs.get_type() == Type_Enum.undefined:
            raise AST_Runtime_Error("{}: Left hand expression is undefined".format(type(self)))

        elif data_rhs.get_type() == Type_Enum.undefined:
            raise AST_Runtime_Error("{}: Right hand expression is undefined".format(type(self)))

        else:
            raise AST_Runtime_Error("{}: No matching method for ({} + {})".format(type(self), data_lhs.get_type(), data_rhs.get_type()))

        return node_ret


class AST_Expression_Subtraction(AST_Expression):
    """

    """

    def __init__(self) -> None:
        super(AST_Node, self).__init__()
        self._expected_nodes = [AST_Expression, AST_Expression]

    def affix_nodes(self, expression_lhs: AST_Expression, expression_rhs: AST_Expression) -> None:
        self._affixed_nodes = [expression_lhs, expression_rhs]
        self.verify_node()

    def walk(self, name_space: Name_Space) -> AST_Data:
        node_ret = AST_Data()
        
        data_lhs = self._affixed_nodes[0].walk(name_space)
        data_rhs = self._affixed_nodes[1].walk(name_space)

        if (data_lhs.get_type() in (Type_Enum.int, Type_Enum.float, Type_Enum.bool) and # Subtract numbers
                data_rhs.get_type() in (Type_Enum.int, Type_Enum.float, Type_Enum.bool)):
            node_ret.set_value(data_lhs.get_value() - data_rhs.get_value())

            if (data_lhs.get_type() == Type_Enum.float or # Check for floating-point
                    data_rhs.get_type() == Type_Enum.float):
                node_ret.set_type(Type_Enum.float)
            else:
                node_ret.set_type(Type_Enum.int)

        elif data_lhs.get_type() == Type_Enum.undefined:
            raise AST_Runtime_Error("{}: Left hand expression is undefined".format(type(self)))

        elif data_rhs.get_type() == Type_Enum.undefined:
            raise AST_Runtime_Error("{}: Right hand expression is undefined".format(type(self)))

        else:
            raise AST_Runtime_Error("{}: No matching method for ({} - {})".format(type(self), data_lhs.get_type(), data_rhs.get_type()))

        return node_ret


class AST_Expression_Multiplication(AST_Expression):
    """

    """

    def __init__(self) -> None:
        super(AST_Node, self).__init__()
        self._expected_nodes = [AST_Expression, AST_Expression]

    def affix_nodes(self, expression_lhs: AST_Expression, expression_rhs: AST_Expression) -> None:
        self._affixed_nodes = [expression_lhs, expression_rhs]
        self.verify_node()

    def walk(self, name_space: Name_Space) -> AST_Data:
        node_ret = AST_Data()
        
        data_lhs = self._affixed_nodes[0].walk(name_space)
        data_rhs = self._affixed_nodes[1].walk(name_space)

        if (data_lhs.get_type() in (Type_Enum.int, Type_Enum.float, Type_Enum.bool) and # Multiply numbers
                data_rhs.get_type() in (Type_Enum.int, Type_Enum.float, Type_Enum.bool)):
            node_ret.set_value(data_lhs.get_value() * data_rhs.get_value())

            if (data_lhs.get_type() == Type_Enum.float or # Check for floating-point
                    data_rhs.get_type() == Type_Enum.float):
                node_ret.set_type(Type_Enum.float)
            else:
                node_ret.set_type(Type_Enum.int)

        elif data_lhs.get_type() == Type_Enum.undefined:
            raise AST_Runtime_Error("{}: Left hand expression is undefined".format(type(self)))

        elif data_rhs.get_type() == Type_Enum.undefined:
            raise AST_Runtime_Error("{}: Right hand expression is undefined".format(type(self)))

        else:
            raise AST_Runtime_Error("{}: No matching method for ({} * {})".format(type(self), data_lhs.get_type(), data_rhs.get_type()))

        return node_ret


class AST_Expression_Division(AST_Expression):
    """

    """

    def __init__(self) -> None:
        super(AST_Node, self).__init__()
        self._expected_nodes = [AST_Expression, AST_Expression]

    def affix_nodes(self, expression_lhs: AST_Expression, expression_rhs: AST_Expression) -> None:
        self._affixed_nodes = [expression_lhs, expression_rhs]
        self.verify_node()

    def walk(self, name_space: Name_Space) -> AST_Data:
        node_ret = AST_Data()

        data_lhs = self._affixed_nodes[0].walk(name_space)
        data_rhs = self._affixed_nodes[1].walk(name_space)

        if (data_lhs.get_type() in (Type_Enum.int, Type_Enum.float, Type_Enum.bool) and # Divide numbers
                data_rhs.get_type() in (Type_Enum.int, Type_Enum.float, Type_Enum.bool)):
            if data_rhs.get_value() == 0:
                raise AST_Runtime_Error("{}: Cannot divide by zero".format(type(self)))

            node_ret.set_value(data_lhs.get_value() / data_rhs.get_value())
            node_ret.set_type(Type_Enum.float)

        elif data_lhs.get_type() == Type_Enum.undefined:
            raise AST_Runtime_Error("{}: Left hand expression is undefined".format(type(self)))

        elif data_rhs.get_type() == Type_Enum.undefined:
            raise AST_Runtime_Error("{}: Right hand expression is undefined".format(type(self)))

        else:
            raise AST_Runtime_Error("{}: No matching method for ({} / {})".format(type(self), data_lhs.get_type(), data_rhs.get_type()))

        return node_ret


class AST_Expression_Power(AST_Expression):
    """

    """

    def __init__(self) -> None:
        super(AST_Node, self).__init__()
        self._expected_nodes = [AST_Expression, AST_Expression]

    def affix_nodes(self, expression_lhs: AST_Expression, expression_rhs: AST_Expression) -> None:
        self._affixed_nodes = [expression_lhs, expression_rhs]
        self.verify_node()

    def walk(self, name_space: Name_Space) -> AST_Data:
        node_ret = AST_Data()

        data_lhs = self._affixed_nodes[0].walk(name_space)
        data_rhs = self._affixed_nodes[1].walk(name_space)

        if (data_lhs.get_type() in (Type_Enum.int, Type_Enum.float, Type_Enum.bool) and # Divide numbers
                data_rhs.get_type() in (Type_Enum.int, Type_Enum.float, Type_Enum.bool)):
            node_ret.set_value(data_lhs.get_value() ** data_rhs.get_value())

            if (data_lhs.get_type() == Type_Enum.float or # Check for floating-point
                    data_rhs.get_type() == Type_Enum.float):
                node_ret.set_type(Type_Enum.float)
            else:
                node_ret.set_type(Type_Enum.int)

        elif data_lhs.get_type() == Type_Enum.undefined:
            raise AST_Runtime_Error("{}: Left hand expression is undefined".format(type(self)))

        elif data_rhs.get_type() == Type_Enum.undefined:
            raise AST_Runtime_Error("{}: Right hand expression is undefined".format(type(self)))

        else:
            raise AST_Runtime_Error("{}: No matching method for ({} ** {})".format(type(self), data_lhs.get_type(), data_rhs.get_type()))

        return node_ret


### ======================================== Block_List / Statement / Expression / Literal ======================================== ###


class AST_Literal(AST_Expression):
    """

    """

    def __init__(self, data_value, data_type: int) -> None:
        super(AST_Node, self).__init__()
        self._data = AST_Data()
        self._data.set_value(data_value)
        self._data.set_type(data_type)

    def walk(self, name_space: Name_Space) -> AST_Data:
        return self._data


### ======================================== Block_List / Statement / Expression / Identity ======================================== ###


class AST_Identifier(AST_Expression):
    """

    """

    def __init__(self, name) -> None:
        super(AST_Node, self).__init__()
        self._name = name

    def walk(self, name_space: Name_Space) -> AST_Data:
        return name_space.get(self._name)


### ======================================== Block_List / Statement / Expression / Function ======================================== ###


class AST_Function(AST_Expression):
    """

    """

    def __init__(self) -> None:
        super(AST_Node, self).__init__()

    def walk(self, name_space: Name_Space) -> AST_Data:
        return AST_Data()


class AST_Function_Print(AST_Expression):
    """

    """

    def __init__(self) -> None:
        super(AST_Node, self).__init__()
        self._expected_nodes = [AST_Expression]

    def affix_nodes(self, expression: AST_Expression) -> None:
        self._affixed_nodes = [expression]
        self.verify_node()

    def walk(self, name_space: Name_Space) -> AST_Data:
        data = self._affixed_nodes[0].walk(name_space)

        print("AST_Print: type: {}  value: {}".format(data.get_type(), data.get_value()))

        return AST_Data()