import scipy.io as spio
import math

# load raw data
mat = spio.loadmat('cleandata_students.mat', squeeze_me=True)

# extract labels and examples from raw data
labels = mat['y'] # N labels
examples = mat['x'] # N examples of 45 attributes each.


def entropy(positive_count, negative_count):
    """ Returns the entropy of the positive and negative counts """

    # get the proportion of negative and positive examples
    pos_proportion = float(positive_count)/(positive_count + negative_count)
    neg_proportion = float(negative_count)/(positive_count + negative_count)
    
    return -pos_proportion*math.log(pos_proportion, 2) - neg_proportion*math.log(neg_proportion, 2)

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
    print pos_targets, neg_targets
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

# test
binary_targets = map(lambda x: int(x == 1), labels)
print choose_best_decision_attribute(examples, range(45), binary_targets)
