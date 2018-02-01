from math import log

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
