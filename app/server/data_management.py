import scipy.io
import numpy as np

def read_and_partition_data():
    '''
    :return: Xtrain, Xtest, Ttrain, Ttest

    Read the data and partition it into training and testing sets
    '''
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

    # Fix the samples without vehicle types, giving them an appropriate type
    T = fix_vehicle_type_specials(T)

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

def fix_vehicle_type_specials(T):
    '''
    :param T: Class name from a single target value
    :return:  Class name, whether updated with appropriate vehicle type or not

    The 16 vehicles without appropriate vehicle types are fixed giving them
    a class. These 16  types are seen in the nasty if/else block below
    '''

    specials = []
    types = ['Cab', 'Sedan', 'Minivan', 'Van', 'Coupe', 'Convertible', 'Wagon', 'Hatchback', 'SUV', ]

    for class_name in T:
        words = class_name[0].split()
        type = words[-2]

        # Change type from 'Cab' to 'Truck' for clarity
        if type == 'Cab':
            words.insert(-1, 'Truck')
            class_name[0] = ' '.join(words)

        # For each special case, add the true vehicle type
        if type not in types:
            if class_name[0] == 'Chevrolet Corvette ZR1 2012':
                words.insert(-1, 'Coupe')
            if class_name[0] == 'Buick Regal GS 2012':
                words.insert(-1, 'Sedan')
            if class_name[0] == 'Dodge Charger SRT-8 2009':
                words.insert(-1, 'Sedan')
            if class_name[0] == 'Acura TL Type-S 2008':
                words.insert(-1, 'Sedan')
            if class_name[0] == 'Jaguar XK XKR 2012':
                words.insert(-1, 'Coupe')
            if class_name[0] == 'Chevrolet HHR SS 2010':
                words.insert(-1, 'Wagon')
            if class_name[0] == 'Lamborghini Gallardo LP 570-4 Superleggera 2012':
                words.insert(-1, 'Coupe')
            if class_name[0] == 'Chevrolet TrailBlazer SS 2009':
                words.insert(-1, 'SUV')
            if class_name[0] == 'Chevrolet Corvette Ron Fellows Edition Z06 2007':
                words.insert(-1, 'Coupe')
            if class_name[0] == 'Chrysler 300 SRT-8 2010':
                words.insert(-1, 'Sedan')
            if class_name[0] == 'FIAT 500 Abarth 2012':
                words.insert(-1, 'Hatchback')
            if class_name[0] == 'Ford Ranger SuperCab 2011':
                words.insert(-1, 'Truck')
            if class_name[0] == 'Chevrolet Cobalt SS 2010':
                words.insert(-1, 'Coupe')
            if class_name[0] == 'Infiniti G Coupe IPL 2012':
                words.insert(-1, 'Coupe')
            if class_name[0] == 'Dodge Challenger SRT8 2011':
                words.insert(-1, 'Coupe')
            if class_name[0] == 'Acura Integra Type R 2001':
                words.insert(-1, 'Coupe')

            class_name[0] = ' '.join(words)

    return T