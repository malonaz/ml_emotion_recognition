from training import *
from evaluation import *

# the array is assumed to be either of proababilities of dependencies
def append_array(filename, anArray):
    f = open(filename, 'a')
    for row in range(anArray.shape[0]):
        for col in range(anArray.shape[1]):
            f.write( '%-4s ' % (anArray[row,col]))
        f.write('\n')
    f.write('\n\n')
    f.close()
#Function to write a list to a results file
def append_list(filename, aList):
    f = open(filename, 'a')
    for row in range(aList.shape[0]):
        f.write( '%6.3f ' % (aList[row]))
    f.write('\n\n')
    f.close()
#Function to write a string to a results file
def append_string(filename, aString):
    f = open(filename, 'a')
    f.write('%s\n' % (aString))
    f.close()

    
def main():
    # we will write results to this file
    filename = "output/results.txt"

    # erase file
    open(filename, 'w').close()

    # 1. write title of file 
    append_string(filename, "Results for Machine Learning Coursework by Malon AZRIA, Alexandre CODACCIONI, Benjamin MAI & Laura HAGEGE")

    # 2. get clean data set
    examples, labels = load_data(CLEAN_DATA_STUDENTS)
    append_string(filename, "Loaded clean dataset")
    
    # 3. train 6 trees on the clean dataset
    # trained_trees = train_trees(examples, labels)

    # 4. generate graphs in (Graphs folder) for each tree
    # visualize_trees(trained_trees)

    # 5. perform cross_validation
    confusion_matrix, average_error_rate = cross_validation(examples, labels)
    append_string(filename, "performed cross_validation")

    # 6. print confusion matrix
    append_string(filename, "confusion matrix")
    append_array(filename, confusion_matrix)

    # 7. get recall and precision rates
    recall_rates, precision_rates = get_recall_precision_rates(confusion_matrix)

    # 8. print recall rates
    append_string(filename, "recall rates")
    append_list(filename, recall_rates)

    # 9. print precision rates
    append_string(filename, "precision rates")
    append_list(filename, precision_rates)

    # 10. print average classification rate
    append_string(filename, "average classification rate")
    append_string(filename, str(1 - average_error_rate))

    
if __name__ == "__main__":
    main()


    
