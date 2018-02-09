from pickle import dump, load



def save_trees_to_pickle(trees, dataset):
    """ saves pickle-serialized copies of the trees."""

    for emotion in range(1, 7):

        # extract tree
        tree = trees[emotion - 1]
        
        # open file in binary mode
        f = open("pickled_trees/" + dataset + "/emotion" + str(emotion) + ".p", "wb")
        
        # use pickle to generate and save pickle-serialized tree
        dump(tree, f)
        
        # close file
        f.close()



def load_trees_from_pickle(dataset):
    """ Loads and returns the six pickled trees of the given dataset."""

    # used to store the trees
    trees = []
    
    for emotion in range(1, 7):
        
        # open file in binary mode
        f = open("pickled_trees/" + dataset + "/emotion" + str(emotion) + ".p", "rb")

        # load the tree and add it to the trees container
        tree = load(f)
        trees.append(tree)

        # close file
        f.close()
        
    return trees

def load_all_trees():
    """" Loads and returns [clean_dataset_trees, noisy_dataset_trees]."""

    clean_dataset_trees = load_trees_from_pickle("clean_dataset")
    noisy_dataset_trees = load_trees_from_pickle("noisy_dataset")

    return clean_dataset_trees, noisy_dataset_trees
