

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


        

        
