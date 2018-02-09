from training import *
from evaluation import *
from pickle_trees import *
from numpy import savetxt, column_stack
import sys

    
def main(dataset = "data/cleandata_students.mat", folder = "test_dataset"):
    """ dataset should be the filepath to the dataset as observed from root directory.
        Do not change the folder. """
    
    # 1. get dataset
    examples, labels = load_data(dataset)

    # 2. train 6 trees on the dataset
    trained_trees = train_trees(examples, labels)

    # 3. save trees in pickle format. comment out if you wish to do so
    save_trees_to_pickle(trained_trees, folder)
                
    # 5. generate graphs in (graphs folder) for each tree
    visualize_trees(trained_trees, folder)

    # 6. perform cross_validation
    confusion_matrix, average_error_rate = cross_validation(examples, labels)

    # 8. get recall and precision rates
    recall_rates, precision_rates = get_recall_precision_rates(confusion_matrix)

    # 11. get F_1 measures
    f1_measures = get_f_measures(recall_rates, precision_rates)
    


    
if __name__ == "__main__":
    
    main()

    
