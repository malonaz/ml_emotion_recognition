import scipy.io as spio


mat = spio.loadmat('cleandata_students.mat', squeeze_me=True)

y = mat['y'] # contains a list of integers
x = mat['x'] # contains a list of list of integers


