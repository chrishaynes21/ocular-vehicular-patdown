import scipy.io
import numpy as np

def read_and_partition_data(meta_data_directory = "../../car_devkit/devkit/", seed = 0):
    '''
    :return: Xtrain, Xtest, Ttrain, Ttest

    Read the data and partition it into training and testing sets
    '''
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
        T.append(class_name[0])

    T = np.array(T)

    # Fix the samples without vehicle types, giving them an appropriate type
    T = fix_vehicle_type_specials(T)

    #set the seed if it is not zero.
    if seed:
        np.random.seed(seed)

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

def select_target_class(target, T):
    '''
    :param target: Desired target class to use ('Make', 'Type', or 'Decade')
    :param T: Target Matrix
    :return:  Updated Target matrix with just the desired class

    Updates the target matrix using only the desired class for each sample
    '''

    for class_name in T:
        words = class_name.split()

        if target == 'Make':
            class_name = words[0]

        if target == 'Type':
            class_name = words[-2]

        if target == 'Decade':
            year = int(words[-1])
            century = (int(year / 100)) * 100
            year_in_century = year % 100
            decade = century + (int(year_in_century / 10) * 10)
            class_name = str(decade)
            
def fix_vehicle_type_specials(T):
    '''
    :param T: Class name from a single target value
    :return:  Class name, whether updated with appropriate vehicle type or not

    The 16 vehicles without appropriate vehicle types are fixed giving them
    a class. These 16  types are seen in the nasty if/else block below
    '''

    types = ['Cab', 'Sedan', 'Minivan', 'Van', 'Coupe', 'Convertible', 'Wagon', 'Hatchback', 'SUV', ]
    T_new = np.empty([T.shape[0], 3], dtype=T.dtype)

    i = 0
    for class_name in T:
        words = class_name.split()
        type = words[-2]

        # Change type from 'Cab' to 'Truck' for clarity
        if type == 'Cab':
            words.insert(-1, 'Truck')

        # For each special case, add the true vehicle type
        if type not in types:
            if class_name == 'Chevrolet Corvette ZR1 2012':
                words.insert(-1, 'Coupe')
            if class_name == 'Buick Regal GS 2012':
                words.insert(-1, 'Sedan')
            if class_name == 'Dodge Charger SRT-8 2009':
                words.insert(-1, 'Sedan')
            if class_name == 'Acura TL Type-S 2008':
                words.insert(-1, 'Sedan')
            if class_name == 'Jaguar XK XKR 2012':
                words.insert(-1, 'Coupe')
            if class_name == 'Chevrolet HHR SS 2010':
                words.insert(-1, 'Wagon')
            if class_name == 'Lamborghini Gallardo LP 570-4 Superleggera 2012':
                words.insert(-1, 'Coupe')
            if class_name == 'Chevrolet TrailBlazer SS 2009':
                words.insert(-1, 'SUV')
            if class_name == 'Chevrolet Corvette Ron Fellows Edition Z06 2007':
                words.insert(-1, 'Coupe')
            if class_name == 'Chrysler 300 SRT-8 2010':
                words.insert(-1, 'Sedan')
            if class_name == 'FIAT 500 Abarth 2012':
                words.insert(-1, 'Hatchback')
            if class_name == 'Ford Ranger SuperCab 2011':
                words.insert(-1, 'Truck')
            if class_name == 'Chevrolet Cobalt SS 2010':
                words.insert(-1, 'Coupe')
            if class_name == 'Infiniti G Coupe IPL 2012':
                words.insert(-1, 'Coupe')
            if class_name == 'Dodge Challenger SRT8 2011':
                words.insert(-1, 'Coupe')
            if class_name == 'Acura Integra Type R 2001':
                words.insert(-1, 'Coupe')

        # Remove everything in string leaving it as '<Make> <Type> <Year>'
        targets = np.array([words[0], words[-2], words[-1]]).reshape((1, 3))
        T_new[i, :] = targets[:, :]
        i += 1

    return T_new

def get_classname(class_int, classification_type):

    if classification_type == "bodystyle":
        #declare hardcoded array
        body_styles = ['Convertible', 'Coupe', 'Hatchback', 'Minivan', 'SUV', 'Sedan',
        'Truck', 'Van', 'Wagon']
        return body_styles[class_int]
        
    elif classification_type == "make":
        makes = ['AM', 'Acura', 'Aston', 'Audi', 'BMW', 'Bentley', 'Bugatti',
        'Buick', 'Cadillac', 'Chevrolet', 'Chrysler', 'Daewoo', 'Dodge',
        'Eagle', 'FIAT', 'Ferrari', 'Fisker', 'Ford', 'GMC', 'Geo',
        'HUMMER', 'Honda', 'Hyundai', 'Infiniti', 'Isuzu', 'Jaguar',
        'Jeep', 'Lamborghini', 'Land', 'Lincoln', 'MINI', 'Maybach',
        'Mazda', 'McLaren', 'Mercedes-Benz', 'Mitsubishi', 'Nissan',
        'Plymouth', 'Porsche', 'Ram', 'Rolls-Royce', 'Scion', 'Spyker',
        'Suzuki', 'Tesla', 'Toyota', 'Volkswagen', 'Volvo', 'smart']
        return makes[class_int]
    
    elif classification_type == 'decade':
        #classify decade
        decades = ["1990's", "2000's", "2010's"]
        return decades[class_int]
    
    else:
        return 'invalid classification type'

