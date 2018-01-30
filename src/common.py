import scipy.io as spio
import math
import random

##### HELPER FUNCTIONS
def entropy(positive_count, negative_count):
    """ Returns the entropy of the positive and negative counts """

    if (positive_count == 0 or negative_count == 0):
        # no entropy!
        return 0
    
    
    # get weights of negative and positive examples
    pos_weight = float(positive_count)/(positive_count + negative_count)
    neg_weight = float(negative_count)/(positive_count + negative_count)

    # compute entropy
    return -pos_weight*math.log(pos_weight, 2) - neg_weight*math.log(neg_weight, 2)
        

def information_remainder(examples, attribute_index, binary_targets):
    """ Returns the information gained by classifying the examples on the given attribute.
    @params:
        examples: the examples we wish to classify
        attribute_index: index of the attribute used to split the data
        binary_targets: contains binary target for each example, where a 1 indicates the example
                        is a positive match.
    """

    # format: [num of examples that are a class match, num of examples that are not]
    pos_attribute = [0, 0]
    neg_attribute = [0, 0]
    
    for i in range(len(examples)):
        # get example
        example = examples[i]
        
        if (example[attribute_index] == 1):
            # example has attribute.
            pos_attribute[binary_targets[i]] +=1
            
        else:
            # example does not have attribute
            neg_attribute[binary_targets[i]] += 1

    # get entropy of examples with positive attribute
    pos_entropy = entropy(pos_attribute[0], pos_attribute[1])
    neg_entropy = entropy(neg_attribute[0], neg_attribute[1])

    # get total positive and total negative attributes
    pos_count = float(sum(pos_attribute))
    neg_count = float(sum(neg_attribute))

    # get weight of positive attributes
    pos_weight = pos_count/(pos_count + neg_count)
    neg_weight = neg_count/(pos_count + neg_count)
    
    # debug print
    #print "attribute " + str(attribute_index) + ": " + str(pos_attribute) + ", " + str(neg_attribute) + ", " + \
    #    str(pos_weight*pos_entropy + neg_weight*neg_entropy)
    
    # return remainder entropy
    return pos_weight*pos_entropy + neg_weight*neg_entropy


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
    

