from data_loader import *
from training import *
from random import randrange
from random import seed
from numpy import zeros

##### PART III: EVALUATION

def get_k_folds(examples, labels, k = 10):
    """ Splits the given data into k folds and returns it as a list."""

    # seed random
    seed(345)

    # convert examples to list. (they might be in numpy array format). this does not modify originals!
    examples = list(examples)
    labels = list(labels)
    
    # used to store the k folds
    k_folds = []
    
    # size of a fold
    fold_size = len(examples)/k

    for i in range(k - 1):
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

    # now add the rest to the last fold
    k_folds.append([examples, labels])
    
    return k_folds


def random_tiebreaker(pos_predictions):
    """ breaks a tie by simply return a random positive prediction."""
    
    # generate a random index of the non-empty pos_prediction list
    random_index = randrange(len(pos_predictions))

    return pos_predictions[random_index][0]


def deepest_tiebreaker(pos_predictions):
    """ breaks a tie by return the prediction that was found at the deepest node."""

    # find deepest level
    deepest_level = max(pos_predictions, key = lambda (emotion, level): level)[1]
    
    # keep only emotions with the deepest level
    deep_pos_predictions = filter(lambda (emotion, level): level == deepest_level, pos_predictions)

    # break ties randomly, in case there are two candidates
    return random_tiebreaker(deep_pos_predictions)


def lowest_tiebreaker(pos_predictions):
    """ breaks a tie by return the prediction that was found at the most shallow node."""

    # find lowest level
    most_shallow_level = min(pos_predictions, key = lambda (emotion, level): level)[1]
    
    # keep only emotions with the deepest level
    shallow_pos_predictions = filter(lambda (emotion, level): level == most_shallow_level, pos_predictions)

    # break ties randomly, in case there are two candidates
    return random_tiebreaker(shallow_pos_predictions)



def classify_example(trees, example, tiebreaker_function = lowest_tiebreaker):
    """ returns a prediction of the example's class using the given trees,
        uses the given tie break to break up any tie."""

    # get each tree's classification of the given example
    predictions = map(lambda tree: tree.evaluate(example), trees)

    # get the emotions of predictions that are a match along with the depth at which they were found
    pos_predictions = [(i + 1, predictions[i][1]) for i in range(len(predictions)) if predictions[i][0]]

    if (pos_predictions == []):
        # no match with any tree. return random value between 1 and 6
        return randrange(1, 7)

    # use given tiebreaker_function
    return tiebreaker_function(pos_predictions)


def test_trees(trees, examples):
    """ takes trained trees and a list of examples. Returns a vector of label predictions."""

    # use each tree to classify each example
    predictions = map(lambda example: classify_example(trees, example), examples)

    return predictions


def get_error_rate(predictions, labels):
    """ returns the error rates of the predictions versus the labels."""
    
    # for each data point, check if the tree's evaluation matches its binary_target
    results = [predictions[i] != labels[i] for i in range(len(predictions))]

    # return the ratio of matches to data points
    return float(sum(results))/len(results)



def get_confusion_matrix(predictions, labels):
    """ returns confusion matrix implied by the predictions versus the labels."""

    # create a 6 by 6 matrix filled with 0s
    confusion_matrix = zeros((6, 6), int)

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
    average_error_rate = 0.0

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
        
        # add predictions and test_labels to their respective totals
        total_predictions += predictions
        total_labels += test_labels
        
    # compute confusion matrix
    confusion_matrix = get_confusion_matrix(total_predictions, total_labels)

    # compute average error rate
    average_error_rate  = get_error_rate(total_predictions, total_labels)
    
    return confusion_matrix, average_error_rate


def get_recall_precision_rates(confusion_matrix):
    """ Computes the recall and precision rates for each class and returns
        a list [recall rates, precision rates]. """

    # used to store the recall and precision rates
    recall_rates = zeros(6, float)
    precision_rates = zeros(6, float)
    
    for i in range(confusion_matrix.shape[0]):

        # get the ith row and column
        row = confusion_matrix[i, :]
        col = confusion_matrix[:, i]

        # compute TP, FP and FN
        TP = float(row[i])
        FP = float(sum(col) - TP)
        FN = float(sum(row) - TP)
        
        # compute recall rate and add it to recall rates
        recall_rates[i] = (100*TP)/(TP + FN)

        # compute precision rate and add it to precision rates
        precision_rates[i] = (100*TP)/(TP + FP)

    return recall_rates, precision_rates
        

def get_f_measures(recall_rates, precision_rates, alpha = 1):
    """ Computes the F_a measures of all 6 recall & precision rates duos and returns it. """

    # used to store f1 measures
    f1_measures = zeros(6, float)

    for i in range(len(recall_rates)):

        # get current recall & precision rates
        recall = recall_rates[i]
        precision = precision_rates[i]

        # compute f1_measure and append it to f1_measures
        f1_measure = ((1 + alpha*alpha)*precision*recall)/(alpha*alpha*precision + recall)
        f1_measures[i] = f1_measure

        
    return f1_measures
