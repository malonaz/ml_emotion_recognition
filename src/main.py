from learning import *


def main():

    # train 6 trees on the clean dataset
    trained_trees = train_trees(CLEAN_DATA_STUDENTS)

    # generate graphs in (Graphs folder) for each tree
    visualize_trees(trained_trees)

    



if __name__ == "__main__":
    main()


    
