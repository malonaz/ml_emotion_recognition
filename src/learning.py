from decision_tree import *
from training import *

from helpers import *

from data_loader import *







        
##### PART III: EVALUATION

def train_trees(dataset):
    """ uses the given dataset to train 6 trees, one for each emotion and  
        Returns a list of these six trees."""

    # used to store the trained trees
    trained_trees = []
    
    # get clean data set
    examples, labels = load_data(dataset)

    for i in range(NUM_CLASSES):

        # get emotion number. [1,2,3,4,5,6]
        emotion = i + 1
        
        # generate binary targets for current emotion
        binary_targets = get_binary_targets(labels, emotion)

        # train tree
        trained_tree = decision_tree_learning(examples, range(NUM_ATTRIBUTES), binary_targets)

        # add it to trained trees
        trained_trees.append(trained_tree)

    return trained_trees

def visualize_trees(trees):
    """ generates graphs for each trained tree (one for each emotion) in the graphs folder."""

    for i in range(len(trees)):

        # get emotion number [1, 2, 3, 4, 5, 6]
        emotion = i + 1

        # compute filename
        filename = "graphs/emotion" + str(emotion) + ".dot"

        # generate graph
        trees[i].generate_graph(filename)
    

def test_performance(tree, emotion, test_data, binary_targets):
    """ returns the error rate of the tree classifier on the test data."""

    # for each data point, check if the tree's evaluation matches its binary_target
    results = [tree.evaluate(test_data[i]) == binary_targets[i] for i in range(len(test_data))]

    # return the ratio of matches to data points
    return float(sum(results))/len(results)


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


def test_trained_trees():
    # get trained trees
    trained_trees = train_trees(CLEAN_DATA_STUDENTS, True)

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

    
