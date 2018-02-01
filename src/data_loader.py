from scipy.io import loadmat

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
    mat = loadmat(filename, squeeze_me = True)

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

