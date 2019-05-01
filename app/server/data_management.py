import scipy.io
import numpy as np

def read_and_partition_data():
    meta_data_directory = "../../car_devkit/devkit/"
    meta = scipy.io.loadmat(meta_data_directory + 'cars_meta.mat')
    train_annotations = scipy.io.loadmat(meta_data_directory + 'cars_train_annos.mat')

    # Example of how to see a class
    # [dict][get to element][get string]
    # -> meta['class_names'][0, 0][0]

    # Example of how to get a specific sample
    # x1,x2,y1,y2,class,name
    # -> train_annotations['annotations'][0, 0]

    # another example, third image should be a dodge truck
    # the [4] accesses the class index. [5] would get the image name
    # -> train_annotations['annotations'][0, 2][4][0][0]
    # This returns 91, which corresponds to the location in the metadata file specifying
    # the class for this sample

    # Organize target values (class_names) so they correspond to the order of training values
    T = []
    nrows = len(train_annotations['annotations'][0])

    for i in range(nrows):
        location = train_annotations['annotations'][0, i][4][0][0]
        class_name = meta['class_names'][0, location - 1]
        T.append(class_name)

    T = np.array(T)

    # Partition the data into training and testing sets
    nTrain = int(round(nrows * 0.8))
    nTest = nrows - nTrain
    rows = np.arange(nrows)
    np.random.shuffle(rows)
    trainIndices = rows[:nTrain]
    testIndices = rows[nTrain:]
    Xtrain = train_annotations['annotations'][0, trainIndices]
    Ttrain = T[trainIndices, :]
    Xtest = train_annotations['annotations'][0, testIndices]
    Ttest = T[testIndices, :]

    return Xtrain, Ttrain, Xtest, Ttest