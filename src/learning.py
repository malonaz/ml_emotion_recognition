from helpers import *
from decision_tree import *
import scipy.io as spio
from random import randrange
import math
import sys

#### DATA PARAMETERS
CLEAN_DATA_STUDENTS = "data/cleandata_students.mat"
NOISY_DATA_STUDENTS = "data/noisydata_students.mat"
NUM_ATTRIBUTES = 45
ATTRIBUTE_NUM_VALUES = 2 # we are dealing with binary numbers
NUM_CLASSES = 6

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


##### PART II: TRAINING DECISION TREE
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
    best_attribute_index = choose_best_decision_attribute(examples, attributes, binary_targets)
    remaining_attributes = [attribute for attribute in attributes if attribute != best_attribute_index]

    # new decision tree with root as best_attribute
    tree = DecisionTree(test = best_attribute_index)
    
    # add branch for each value of the best attribute. Here it can only take on two values
    for value in range(ATTRIBUTE_NUM_VALUES):
        
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
        
##### PART III: EVALUATION

def train_trees():
    """ uses the clean dataset provided to train 6 trees, one for each emotion and generate
        graphs for them (in Graph folder). Returns a list of these six trees."""

    # used to store the trained trees
    trained_trees = []
    
    # get clean data set
    examples, labels = load_data(CLEAN_DATA_STUDENTS)

    for i in range(NUM_CLASSES):

        # get emotion number. [1,2,3,4,5,6]
        emotion = i + 1
        
        # generate binary targets for current emotion
        binary_targets = get_binary_targets(labels, emotion)

        # train tree
        trained_tree = decision_tree_learning(examples, range(NUM_ATTRIBUTES), binary_targets)

        # generate a graph for this tree
        filename = "graphs/emotion" + str(emotion) + ".dot"
        trained_tree.generate_graph(filename)

        # add it to trained trees
        trained_trees.append(trained_tree)

    return trained_trees


def test_performance(tree, emotion, test_data, binary_targets):
    """ returns the error rate of the tree classifier on the test data."""

    tests_passed = 0
    
    for i in range(len(test_data)):
        tree_result = tree.evaluate(test_data[i])
        real_result = binary_targets[i]
        
        if tree_result == real_result:
            tests_passed += 1
            
    return float(tests_passed)/len(test_data)
    

def classify_example(trees, example):
    """ returns a list of each tree's classification of the given example."""
    return map(lambda tree: tree.evaluate(example), trees)


def test_trees(trees, examples):
    """ takes trained treesa and a list of examples. Returns a vector of label predictions."""

    # use each tree to classify each example
    trees_result = map(lambda example: classify_example(trees, example), examples)
    print tree_result

##### TESTING

def test_decision_tree_learning():
    # get matlab data
    examples, labels = load_data("cleandata_students.mat")

    # generate binary target for emotion 1
    binary_targets = get_binary_targets(labels, 1)
    
    tree = decision_tree_learning(examples, range(NUM_ATTRIBUTES), binary_targets)
    
    return tree

# test_decision_tree_learning()

        
def test_choose_best_decision_attribute():

    # get matlab data
    examples, labels = load_data(CLEAN_DATA_STUDENT)

    # generate binary target for emotion 1
    binary_targets = get_binary_targets(labels, 6)

    # find index of best attribute
    print choose_best_decision_attribute(examples, range(NUM_ATTRIBUTES), binary_targets)


# call to test
#test_choose_best_decision_attribute()



def test_print_graph():
    # get matlab data
    examples, labels = load_data(CLEAN_DATA_STUDENTS)

    # generate binary target for emotion 1
    binary_targets = get_binary_targets(labels, 1)
    
    tree = decision_tree_learning(examples, range(NUM_ATTRIBUTES), binary_targets)
    tree.generate_graph("graphs/graph.dot")

#test_print_graph()


def test_trained_trees():
    # get trained trees
    trained_trees = train_trees()

    # get examples and labels
    examples, labels = load_data(CLEAN_DATA_STUDENTS)

    for example in examples:
        # evalue the current example through all 6 trained trees
        results = map(lambda tree: tree.evaluate(example),trained_trees)

    
#test_trained_trees()

def test_test_performance():
    # get matlab data
    examples, labels = load_data(CLEAN_DATA_STUDENTS)

    # split the data k ways
    k_folds = get_k_folds(examples, labels)


    # train on first fold
    examples, labels = k_folds[0]
    
    # generate binary target for emotion 1
    binary_targets = get_binary_targets(labels, 1)

    # train tree
    tree = decision_tree_learning(examples, range(len(examples[0])), binary_targets)

    # now evaluate the tree using the second fold
    test_examples, test_labels = k_folds[1]

    # generate binay target for emotion 1
    test_binary_targets = get_binary_targets(test_labels, 1)
    
    ans = test_performance(tree, 1, test_examples, test_binary_targets)

    print ans

#test_test_performance()

def main(argv):
    if (len(argv) == 1):
        return 0
    
    if (argv[1] == "graphs"):
        test_trained_trees()
        
    

if __name__ == "__main__":
    main(sys.argv)
    
