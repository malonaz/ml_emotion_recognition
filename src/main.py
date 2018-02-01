from training import *
from evaluation import *

def main():

    # get clean data set
    examples, labels = load_data(CLEAN_DATA_STUDENTS)

    # train 6 trees on the clean dataset
    trained_trees = train_trees(examples, labels)

    # generate graphs in (Graphs folder) for each tree
    visualize_trees(trained_trees)

    

    

if __name__ == "__main__":
    main()


    
