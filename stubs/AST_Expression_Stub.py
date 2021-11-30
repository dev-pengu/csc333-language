from AST.AST_Nodes import *
from sys import maxsize

class AST_Expression_Stub(AST_Expression):
    """
        A test stub which takes the place of a statement
    """

    def __init__(self) -> None:
        super(AST_Node, self).__init__()
        self.times_walked = 0
        self._rid = random.randint(0, maxsize)
        self._affixed_nodes = []
        self._expected_nodes = []
        

    def affix_nodes(self) -> None:
        pass

    def walk(self, name_space: Name_Space) -> AST_Data:
        self.verify_node()
        self.times_walked += 1
        print('\t\texpression ', self._rid , ' times_walked:', self.times_walked)

        d = AST_Data()
        d.set_type(Type_Enum.bool)
        if self.times_walked < 3:
            d.set_value(True)
        else:
            d.set_value(False)

        return d