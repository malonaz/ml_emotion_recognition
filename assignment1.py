import scipy.io as spio
import math
from common import *
from decision_tree import *



##### PART I: LOADING DATA
def load_data(filename):
    """ Returns the labels and examples array from the matlab with the given filename"""

    # load raw data
    mat = spio.loadmat(filename, squeeze_me = True)

    # extract labels and examples from raw data
    examples = mat['x'] # N examples of 45 attributes each.
    labels = mat['y'] # N labels
    
    return examples, labels


def get_binary_targets(labels, label_index):
    """ Returns a list remapping labels according to the given label_index corresponding to an
        and emotion. A 1 indicates a positive example at that index & a 0 indicates a negative
        example.
    @params:
        labels: a list of the labels of the corresponding examples. Labels are numbered 1 to 6, the same as
                the total number of emotions.
        label_index : the emotion you want to map labels to."""

    return map(lambda label: int(label  == label_index), labels)
    

##### PART II: CREATING DECISION TREE
def choose_best_decision_attribute(examples, attributes, binary_targets):
    """ Returns the index of the best decision attribute to classify the examples on.
    @params:
        examples: the examples we wish to classify
        attributes: attributes to consider
        binary_targets: contains binary target for each example, where a 1 indicates the example
                        is a positive match.
    """

    # calculate initial entropy
    pos_targets = sum(binary_targets)
    neg_targets = len(binary_targets) - pos_targets
    initial_entropy = entropy(pos_targets, neg_targets)    
    

    # find the attribute with the smallest information_remainder
    min_remainder_attribute = attributes[0]
    min_remainder = information_remainder(examples, attributes[0], binary_targets)

    for attribute in attributes:
        # get remainder for this attribute
        current_remainder = information_remainder(examples, attribute, binary_targets)
        
        if current_remainder < min_remainder:
            # update remainder info
            min_remainder = current_remainder
            min_remainder_attribute  = attribute

    return min_remainder_attribute

def majority_value(binary_targets):
    """ Returns the mode of binary_targets. """

    # get number of positive and negatives
    pos_count = sum(binary_targets) 
    neg_count = len(binary_targets) - pos_count

    # what about equality?
    return int(pos_count > neg_count)



def decision_tree_learning(examples, attributes, binary_targets):
    """ Returns a decision tree for a given target label."""

    # gather information about parameters
    example_count = len(examples)
    attribute_count = len(attributes)
    pos_count = sum(binary_targets)
    
    # check if examples are already classified
    if (pos_count == 0 or pos_count == example_count):
        # all 1s or 0s. so return leaf node with this value
        return DecisionTree(class_label = binary_targets[0])

    # check if attribute is empty
    if (attribute_count == 0):
        # return a leaf node with mode of binary targets
        return DecisionTree(class_label = majority_value(binary_targets))

    # get the best attribute and the remaining attributes
    best_attribute_index = choose_best_decision_attribute(examples, attributes, binary_targets)
    remaining_attributes = [attribute for attribute in attributes if attribute != best_attribute_index]

    # new decision tree with root as best_attribute
    tree = DecisionTree(test = best_attribute_index)
    
    # add branch for each value of the best attribute. Here it can only take on two values
    for value in range(2):
        
        # get the examples and binary targets that match this value of the best attribute
        examples_i = [examples[i] for i in range(example_count) if examples[i][best_attribute_index] == value]
        binary_targets_i = [binary_targets[i] for i in range(example_count) if examples[i][best_attribute_index] == value]

        if (len(examples_i) == 0):
            # create a leaf node with examples mode value
            leaf = DecisionTree(class_label = majority_value(binary_targets))
            tree.add_kid(leaf)

        else:
            # recursively create a subtree
            subtree = decision_tree_learning(examples_i, remaining_attributes[:], binary_targets_i)
            tree.add_kid(subtree)

    return tree
    
        
    
##### TESTING

def test_decision_tree_learning():
    # get matlab data
    examples, labels = load_data("cleandata_students.mat")

    # generate binary target for emotion 1
    binary_targets = get_binary_targets(labels, 1)
    
    tree = decision_tree_learning(examples, range(45), binary_targets)
    
    return tree

# test_decision_tree_learning()

        
def test_choose_best_decision_attribute():

    # get matlab data
    examples, labels = load_data("cleandata_students.mat")

    # generate binary target for emotion 1
    binary_targets = get_binary_targets(labels, 6)

    # find index of best attribute
    print choose_best_decision_attribute(examples, range(45), binary_targets)


# call to test
#test_choose_best_decision_attribute()



def test_print_graph():
    # get matlab data
    examples, labels = load_data("cleandata_students.mat")

    # generate binary target for emotion 1
    binary_targets = get_binary_targets(labels, 1)
    
    tree = decision_tree_learning(examples, range(45), binary_targets)
    tree.generate_graph()

test_print_graph()
