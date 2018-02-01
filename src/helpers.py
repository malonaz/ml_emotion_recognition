import scipy.io as spio
from math import log
import random


##### HELPER FUNCTIONS



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
            index_to_pop = random.randrange(len(examples))

            # pop the example at this index and append it to current fold examples
            fold_examples.append(examples.pop(index_to_pop))

            # pop the corresponding label and append it to current fold label
            fold_labels.append(labels.pop(index_to_pop))

        # fold is complete. append to k_folds   
        k_folds.append([fold_examples, fold_labels])
        
    return k_folds
    

