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

    # static member to keep count of number of nodes
    node_count = 0
    
    def __init__(self, test = None, class_label = None):
        """ initializes the decision tree """
        
        self.test = test
        self.kids = []
        self.class_label = class_label

        # set id, then increment the static node_count
        self.id = DecisionTree.node_count
        DecisionTree.node_count += 1
        
    def add_kid(self, kid):
        """ adds a kid to the kids field. kid is a DecisionTree."""

        self.kids.append(kid)


    def __str__(self):
        """ overrides the str operator for a decision tree."""

        if self.test != None:
            return "\"test: " + str(self.test) + "\""
            
        return "\"class: " + str(self.class_label) + "\""

    
    def get_id(self):
        """ Returns this node's id."""
        
        return str(self.id)

    def get_label(self):
        """ Returns this node's label for graphing purposes."""
        
        return "[label=" + str(self) + "]"        

    
    def generate_graph(self):
        """ generates a dot file representing this tree."""

        graph_type = "digraph"
        name = "tree_of_class_"
        setup = "node [shape=box, font=Courier]\n"
        root_node = self.get_id() + self.get_label() + "\n" 
        code = root_node + self.get_edges()

        # put text together
        text = "%s %s{\n\n%s\n%s\n}" %(graph_type, name, setup, code)
        
        # open file, write text into it, then close it
        f = open("graph.dot", "w")
        f.write(text)
        f.close()

    
    def get_edges(self):
        """ returns text declaring the nodes and their edges in dot format."""
        
        if (len(self.kids) == 0):
            # leaf node has no edge
            return ""

        #  get the dot declaration of both children
        node_left = self.kids[0].get_id() + self.kids[0].get_label() + "\n"            
        node_right = self.kids[1].get_id() + self.kids[1].get_label() + "\n"

        # get the dot declaration of edges to children
        edge1 = self.get_id() + " -> " + self.kids[0].get_id() + "\n"
        edge2 = self.get_id() + " -> " + self.kids[1].get_id() + "\n"

        # recursively get the kids' node and edges information
        rest = self.kids[0].get_edges() + self.kids[1].get_edges()
        
        return node_left + node_right + edge1 + edge2 + rest
        

    
    
