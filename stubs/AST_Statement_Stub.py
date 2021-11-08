from AST.AST_Nodes import *

class AST_Statement_Stub(AST_Statement):
    """
        A test stub which takes the place of a statement
    """

    def __init__(self, id) -> None:
        super(AST_Node, self).__init__()
        self.id = id
        self.times_walked = 0
        self._affixed_nodes = []
        self._expected_nodes = []


    def affix_nodes(self) -> None:
        pass

    def walk(self, name_space: Name_Space) -> AST_Data:
        self.verify_node()
        self.times_walked += 1
        print('id: {}\twalk count: {}'.format(self.id, self.times_walked))
        return AST_Data()