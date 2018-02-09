from pickle import dump, load



def save_tree_to_pickle(tree, emotion):
    """ saves a pickle-serialized copy of the tree to the given emotion."""

    # open file in binary mode
    f = open("pickled_trees/emotion" + emotion + ".p", "wb")

    # use pickle to generate and save pickle-serialized tree
    dump(tree, f)

    # close file
    f.close()



def load_trees_from_picle():
    """ Loads and returns the six pickled trees."""

    # used to store the trees
    trees = []
    
    for emotion in range(1, 7):
        # open file in binary mode
        f = open("pickled_trees/emotion" + emotion + ".p", "rb")

        # load the tree and add it to the trees container
        tree = load(f)
        trees.append(tree)

        # close file
        f.close()
        
    return trees
