from data_loader import *
from training import *

##### PART III: EVALUATION

def train_trees(examples, labels):
    """ uses the given dataset to train 6 trees, one for each emotion and  
        Returns a list of these six trees."""

    # used to store the trained trees
    trained_trees = []
    

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

