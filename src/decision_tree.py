
class DecisionTree(object):
    """ Represents a decision tree.         
        @members:
           test: the attribute the node is testing. None if node is a leaf node
           kids: node array which contains the subtrees that initiate from this node.
                 empty for leaf nodes
           class_label: Label for the leaf node only, None otherwise. has value 0 or 1
                        for negative-positive respectively, as dictated by the majority
                        of examples.
    """

    # static member to keep count of number of nodes
    node_count = 0
    
    def __init__(self, test = None):
        """ initializes the decision tree """
        
        self.test = test
        self.kids = []

        # set id, then increment the static node_count
        self.id = DecisionTree.node_count
        DecisionTree.node_count += 1
        
    def add_kid(self, kid):
        """ adds a kid to the kids field. kid is a DecisionTree."""

        self.kids.append(kid)


    def evaluate(self, example):
        """ Returns the classification of the given example using this tree."""

        # apply this node's test on the example
        result = example[self.test]

        # recursively go down the appropriate branch of this tree
        return self.kids[result].evaluate(example)

        
    def __str__(self):
        """ overrides the str operator for a decision tree."""

        return "\"AU" + str(self.test + 1) + "\""             

    
    def get_id(self):
        """ Returns this node's id."""
        
        return str(self.id)

    
    def get_label(self):
        """ Returns this node's label for graphing purposes."""
        
        return "[label=" + str(self) + "]"        

    
    def generate_graph(self, filename):
        """ generates a dot file representing this tree with the given filename."""

        graph_type = "digraph"
        name = "tree_of_class_"
        setup = "node [shape=box, font=Courier]\n"
        root_node = self.get_id() + self.get_label() + "\n" 
        code = root_node + self.get_edges()

        # put text together
        text = "%s %s{\n\n%s\n%s\n}" %(graph_type, name, setup, code)
        
        # open file, write text into it, then close it
        f = open(filename, "w")
        f.write(text)
        f.close()

    
    def get_edges(self):
        """ returns text declaring the nodes and their edges in dot format."""

        #  get the dot format information about this subtree's edges
        edges_info = ""
        for i in range(len(self.kids)):
            # get declaration of child node in dot format
            edges_info += self.kids[i].get_id() + self.kids[i].get_label() + "\n"
            # get declaration of edge in dot format
            edges_info += self.get_id() + " -> " + self.kids[i].get_id() + "[label=" + str(i) + "]\n"
            
            # make recursive call to get info about this kid's edge unless its a node
            edges_info += self.kids[i].get_edges()

        return edges_info
    
    
class LeafNode(DecisionTree):
    """ Represents a leaf node in the decision tree
        @members:
           class_label: Label for the leaf node only, None otherwise. has value 0 or 1
                        for negative-positive respectively, as dictated by the majority
                        of examples.
    """

    def __init__(self, class_label):
        """ initializes the leaf node """

        # set member
        self.class_label = class_label

        # call to super constructor 
        super(LeafNode, self).__init__()
    
        
    def evaluate(self, example):
        """ Returns class_label"""

        return self.class_label

    def __str__(self):
        """ overrides the str operator for a leaf node."""
            
        return "\"Decision: " + str(self.class_label) + "\""

