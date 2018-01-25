import scipy.io as spio
import math
from common import *

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
    min_remainder = information_remainder(examples, 0, binary_targets)
    min_remainder_attribute = 0
        
    for i in range(1, len(attributes)):
        # get remainder for this attribute
        current_remainder = information_remainder(examples, i, binary_targets)
        
        if current_remainder < min_remainder:
            # update remainder info
            min_remainder = current_remainder
            min_remainder_attribute  = i
                    
    return min_remainder_attribute

def majority_value(binary_targets):
    """ Returns the mode of binary_targets. """

    # get number of positive and negatives
    pos = sum(binary_targets) 
    neg = len(binary_targets) - pos

    # what about equality?
    return int(pos > neg)

    
##### TESTING
def test_choose_best_decision_attribute():

    # get matlab data
    examples, labels = load_data("cleandata_students.mat")

    # generate binary target for emotion 1
    binary_targets = get_binary_targets(labels, 1)

    # find index of best attribute
    print choose_best_decision_attribute(examples, range(45), binary_targets)


# call to test
test_choose_best_decision_attribute()
