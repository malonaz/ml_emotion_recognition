from print_tree import *

class DecisionTree:
    """ Represents a decision tree.         
        @members:
           test: the attribute the node is testing. None if node is a leaf node
           kids: node array which contains the subtrees that initiate from this node.
                 empty for leaf nodes
           class_label: Label for the leaf node only, None otherwise. has value 0 or 1
                        for negative-positive respectively, as dictated by the majority
                        of examples.
    """

    def __init__(self, test = None, class_label = None):
        """ initializes the decision tree """
        
        self.test = test
        self.kids = []
        self.class_label = class_label
        self.label = None


    def set_label(self, label):
        """ set this label to the given label. """

        self.label = label


    def add_kid(self, kid):
        """ adds a kid to the kids field. kid is a DecisionTree."""

        self.kids.append(kid)


    def __str__(self):
        """ overrides the str operator for a decision tree."""

        if self.test:
            return str(self.test)
        
        return str(self.class_label)


    def generate_graph(self):
        """ generates a dot file representing this tree."""

        # open file, write code into it, then close it
        f = open("graph.dot", "w")
        f.write(get_graph(self))
        f.close()

        
