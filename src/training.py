from data_loader import *
from decision_tree import *
from random import randrange
from math import log

##### PART II: TRAINING DECISION TREE
def entropy(binary_targets):
    """ Returns the entropy of the given binary targets """

    # get pos and neg count
    pos_count = sum(binary_targets)
    neg_count = len(binary_targets) - pos_count
    
    if (pos_count == 0 or neg_count == 0):
        # no entropy!
        return 0
    
    # get weights of negative and positive examples
    pos_weight = float(pos_count)/(pos_count + neg_count)
    neg_weight = float(neg_count)/(pos_count + neg_count)

    # compute entropy
    return -pos_weight*log(pos_weight, 2) - neg_weight*log(neg_weight, 2)

def information_remainder(examples, attribute_index, binary_targets):
    """ Returns the information gained by classifying the examples on the given attribute.
    @params:
        examples: the examples we wish to classify
        attribute_index: index of the attribute used to split the data
        binary_targets: contains binary target for each example, where a 1 indicates the example
                        is a positive match.
    """

    # separate the binary targets that have the given attribute from those who don't
    pos = [binary_targets[i] for i in range(len(examples)) if examples[i][attribute_index]]
    neg = [binary_targets[i] for i in range(len(examples)) if not examples[i][attribute_index]]
    
    # get entropy of examples with positive attribute
    pos_entropy = entropy(pos)
    neg_entropy = entropy(neg)

    # get total positive and total negative attributes
    pos_count = float(len(pos))
    neg_count = float(len(neg))

    # get weight of positive attributes
    pos_weight = pos_count/(pos_count + neg_count)
    neg_weight = neg_count/(pos_count + neg_count)
        
    # return weighted average entropy
    return pos_weight*pos_entropy + neg_weight*neg_entropy

def choose_best_decision_attribute(examples, attributes, binary_targets):
    """ Returns the index of the best decision attribute to classify the examples on.
    @params:
        examples: the examples we wish to classify
        attributes: attributes to consider
        binary_targets: contains binary target for each example, where a 1 indicates the example
                        is a positive match.
    """

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

    if pos_count == neg_count:
       # generate random number 
        return randrange(0, 2)
    
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
    best_attribute = choose_best_decision_attribute(examples, attributes, binary_targets)
    remaining_attributes = [attribute for attribute in attributes if attribute != best_attribute]

    # new decision tree with root as best_attribute
    tree = DecisionTree(test = best_attribute)
    
    # add branch for each value of the best attribute. Here it can only take on two values
    for value in range(ATTRIBUTE_NUM_VALUES):
        
        # get the examples and binary targets that match this value of the best attribute
        examples_i = [examples[i] for i in range(example_count) if examples[i][best_attribute] == value]
        binary_targets_i = [binary_targets[i] for i in range(example_count) if examples[i][best_attribute] == value]

        if (len(examples_i) == 0):
            # return leaf node with examples mode value
            return DecisionTree(class_label = majority_value(binary_targets))

        else:
            # recursively create a subtree
            subtree = decision_tree_learning(examples_i, remaining_attributes[:], binary_targets_i)
            tree.add_kid(subtree)

    return tree    
