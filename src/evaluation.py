from data_loader import *
from training import *
from random import randrange

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


def get_k_folds(examples, labels, k = 10):
    """ Splits the given data into k folds and returns it as a list."""

    # convert examples to list. (they might be in numpy array format). this does not modify originals!
    examples = list(examples)
    labels = list(labels)
    
    # used to store the k folds
    k_folds = []
    
    # size of a fold
    fold_size = len(examples)/k

    for i in range(k):
        fold_examples = []
        fold_labels = []
        
        while (len(fold_examples) < fold_size):

            # generate a random index of examples
            index_to_pop = randrange(len(examples))

            # pop the example at this index and append it to current fold examples
            fold_examples.append(examples.pop(index_to_pop))

            # pop the corresponding label and append it to current fold label
            fold_labels.append(labels.pop(index_to_pop))

        # fold is complete. append to k_folds   
        k_folds.append([fold_examples, fold_labels])
        
    return k_folds
            

def test_performance(tree, emotion, test_data, binary_targets):
    """ returns the error rate of the tree classifier on the test data."""

    # for each data point, check if the tree's evaluation matches its binary_target
    results = [tree.evaluate(test_data[i]) == binary_targets[i] for i in range(len(test_data))]

    # return the ratio of matches to data points
    return float(sum(results))/len(results)


def classify_example(trees, example):
    """ returns a prediction of the example's class using the given trees."""

    # get each tree's classification of the given example
    predictions = map(lambda tree: tree.evaluate(example), trees)

    # get the indices of predictions that are a match
    pos_predictions = [i + 1 for i in range(len(predictions)) if predictions[i]]

    if (pos_predictions == []):
        # no match with any tree. return random value between 1 and 6
        return randrange(1, 7)

    # generate a random index of the non-empty pos_prediction list
    random_index = randrange(len(pos_predictions))

    return pos_predictions[random_index]



def test_trees(trees, examples):
    """ takes trained trees and a list of examples. Returns a vector of label predictions."""

    # use each tree to classify each example
    predictions = map(lambda example: classify_example(trees, example), examples)

    return predictions


def get_error_rate(predictions, labels):
    """ returns the error rates of the predictions versus the labels."""
    
    # for each data point, check if the tree's evaluation matches its binary_target
    results = [predictions[i] == labels[i] for i in range(len(predictions))]

    # return the ratio of matches to data points
    return float(sum(results))/len(results)



def get_confusion_matrix(predictions, labels):
    """ returns confusion matrix implied by the predictions versus the labels."""

    # create a 6 by 6 matrix filled with 0s
    confusion_matrix = [[0 for x in range(6)] for y in range(6)] 

    for i in range(len(predictions)):

        # get the actual and predicted for prediction
        actual = labels[i]
        predicted = predictions[i]

        # increment the appropriate 
        confusion_matrix[actual - 1][predicted - 1] += 1
    
    return confusion_matrix
    
    
def cross_validation(examples, labels, k = 10):
    """ performs k-fold cross validations.
        Returns confusion matrix and average error rate"""

    # get k_folds
    k_folds = get_k_folds(examples, labels, k)

    # used to store the average error rate
    average_error_rate = 0

    # used to store total predictions and total test labels
    total_predictions = []
    total_labels = []
    
    for i in range(k):

        # get test data
        test_examples, test_labels = k_folds[i]

        # get training data
        training_examples = reduce(lambda x, y: x + ([] if y == i else k_folds[y][0]), range(k), [])
        training_labels = reduce(lambda x, y: x + ([] if y == i else k_folds[y][1]), range(k), [])

        # train trees of trained data
        trained_trees = train_trees(training_examples, training_labels)

        # get predictions using trained trees
        predictions = test_trees(trained_trees, test_examples)
        
        # compute error rate add it to the total error rate
        average_error_rate += get_error_rate(predictions, test_labels)/k

        # add predictions and test_labels to their respective totals
        total_predictions += predictions
        total_labels += test_labels
        
    # compute confusion matrix
    confusion_matrix = get_confusion_matrix(total_predictions, total_labels)
    
    return confusion_matrix, average_error_rate
