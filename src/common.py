import scipy.io as spio
import math

##### HELPER FUNCTIONS
def entropy(positive_count, negative_count):
    """ Returns the entropy of the positive and negative counts """

    if (positive_count == 0):
        left = 0
    else:
        # gget proportion of negative and positive examples
        pos_proportion = float(positive_count)/(positive_count + negative_count)
        left = -pos_proportion*math.log(pos_proportion, 2)


    if (negative_count == 0):
        right = 0
    else:
        # get the proportion of negative examples
        neg_proportion = float(negative_count)/(positive_count + negative_count)
        right = -neg_proportion*math.log(neg_proportion, 2)
    
    return left + right


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

    # get proportion of positive attributes
    pos_proportion = pos_count/(pos_count + neg_count)
    neg_proportion = neg_count/(pos_count + neg_count)
    
    # debug print
    #print "attribute " + str(attribute_index) + ": " + str(pos_attribute) + ", " + str(neg_attribute) + ", " + \
    #    str(pos_proportion*pos_entropy + neg_proportion*neg_entropy)
    
    # return remainder entropy
    return pos_proportion*pos_entropy + neg_proportion*neg_entropy


