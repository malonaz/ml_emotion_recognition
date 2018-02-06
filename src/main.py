from training import *
from evaluation import *
from numpy import savetxt, column_stack

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

    
def main(dataset, folder):
    
    # compute filename using the folder path
    filename = "output/" + folder + "/results.txt"

    # erase file if it already exists
    open(filename, 'w').close()

    # 1. write title of file 
    append_string(filename, "Results for Machine Learning Coursework by Malon AZRIA, Alexandre CODACCIONI, Benjamin MAI & Laura HAGEGE")

    # 2. get dataset
    examples, labels = load_data(dataset)
    append_string(filename, "\nLoaded dataset")
    
    # 3. train 6 trees on the dataset
    trained_trees = train_trees(examples, labels)

    # 4. generate graphs in (graphs folder) for each tree
    visualize_trees(trained_trees, folder)

    # 5. perform cross_validation
    confusion_matrix, average_error_rate = cross_validation(examples, labels)
    append_string(filename, "\nperformed cross_validation")

    # 6. print confusion matrix
    append_string(filename, "\nconfusion matrix")
    append_array(filename, confusion_matrix)

    # 7. get recall and precision rates
    recall_rates, precision_rates = get_recall_precision_rates(confusion_matrix)

    # 8. print recall rates
    append_string(filename, "\nrecall rates")
    append_list(filename, recall_rates)

    # 9. print precision rates
    append_string(filename, "\nprecision rates")
    append_list(filename, precision_rates)

    # 10. print F_1 measures
    append_string(filename, "\nf1 measures")
    f1_measures = get_f_measures(recall_rates, precision_rates)
    append_list(filename, f1_measures)
    
    # 10. print average classification rate
    append_string(filename, "\naverage classification rate")
    append_string(filename, str(1 - average_error_rate))



    #########################################################
    # TEX FILES FORMAT
    savetxt("output/" + folder + "/confusion_matrix.txt", confusion_matrix, delimiter = " & ", fmt = "%i")
    savetxt("output/" + folder + "/recall_rates.txt", column_stack(recall_rates), delimiter = " & ", fmt = "%2.2f")
    savetxt("output/" + folder + "/precision_rates.txt", column_stack(precision_rates), delimiter = " & ", fmt = "%2.2f")
    savetxt("output/" + folder + "/f1_measures.txt", column_stack(f1_measures), delimiter = " & ", fmt = "%2.2f")
    

    
if __name__ == "__main__":

    # call with clean data set
    main(CLEAN_DATA_STUDENTS, "clean_dataset")

    # call with clean data set
    main(NOISY_DATA_STUDENTS, "noisy_dataset")


    
