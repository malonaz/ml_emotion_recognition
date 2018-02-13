from training import *
from evaluation import *
from pickle_trees import *
from numpy import savetxt, column_stack
import sys

    
def main(dataset = "data/cleandata_students.mat", folder = "test_dataset"):
    """ dataset should be the filepath to the dataset as observed from root directory.
        Do not change the folder. """
    
    # 1. get dataset. 
    examples, labels = load_data(dataset)

    # 2. get our pickled trees
    trained_clean_trees, trained_noisy_trees = load_all_trees()

    # 3. get prediction vector using test_trees
    predictions = test_trees(trained_clean_trees, examples)

    # 4. get average error rate
    average_error_rate  = get_error_rate(predictions, labels)
    print "average error rate: ", average_error_rate * 100
    
    # 5. get classification rate
    classification_rate = 1 - average_error_rate
    print "classification rate: ", classification rate




    
if __name__ == "__main__":
    
    main()

    
