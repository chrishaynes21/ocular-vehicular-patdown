# Code is written in tf 2.0! Will not work in older versions
import tensorflow as tf
import numpy as np
import data_management
import pickle as pkl


def matlab_to_dict(metadata):
    '''
    :param metadata: the weirdly formatted from matlab numpy array.
            Is part of Xtrain
    :return: a dictionary containing image properties as its values and the jpg name as the key
    '''

    dictionary = {}

    for row in metadata:
        # get coords for top left
        offset_height = row[1][0, 0]
        offset_width = row[0][0, 0]

        # get coord for bottom right
        max_height = row[3][0, 0]
        max_width = row[2][0, 0]

        # calculate offsets from top left to bottom right
        target_height = max_height - offset_height
        target_width = max_width - offset_width

        dictionary[row[5][0]] = {"offset_height": offset_height, "offset_width": offset_width,
                                 "target_height": target_height, "target_width": target_width}

    return dictionary


def crop(input_tensor, metadata):
    '''
    Takes the input tensor and crops it given the parameters in metadata
    :param input_tensor: A tf tensors representing a jpg
    :param metadata: A metadata dict form the function matlab_to_dict
    :return:
    '''
    # get coords for top left
    offset_height = metadata['offset_height']
    offset_width = metadata['offset_width']

    # calculate offsets from top left to bottom right
    target_height = metadata['target_height']
    target_width = metadata['target_width']

    # call the tensorflow crop function.
    cropped = tf.image.crop_to_bounding_box(input_tensor, offset_height, offset_width,
                                            target_height, target_width)
    return cropped


def image_to_numpy(input_image_filepath, height = 275, width = 550):
    '''
    input_image_filepath: a string, defining the path to the image file.

    takes the image as a file path and returns a numpy array.
    the resultant array is fully cropped to the desired size.
    '''

    # Get the raw image using the key as a file name
    raw_image = tf.io.read_file(input_image_filepath)

    # Decode that image as a jpeg
    jpeg_image = tf.io.decode_jpeg(raw_image)

    # pad it to the average h and w from above
    jpeg_image = tf.image.resize_with_pad(jpeg_image, height, width, antialias=True)

    return jpeg_image.numpy().astype(np.uint8)  # <--- maybe a setable parameter?

def make_array_splits(array_length, binsize):
    # Utility function for making batches

    all_indicies = range(0, array_length, binsize)
    all_indicies = list(all_indicies)[1:]
    return all_indicies


def make_batches(X, T, batch_size=1000):
    # Utility function that makes batches based on batch_size

    splits = make_array_splits(X.shape[0], batch_size)
    X_batches = np.split(X, splits)
    T_batches = np.split(T, splits)

    return X_batches, T_batches


def make_pickles(X_batches, T_batches, pickling_dir,
                 path_to_cars_train = "/home/ben/classes/cs445/final/cars_train/",
                 height = 275,
                 width = 550):
    '''
    Writes out the X_batches and T_batches to a pickle file as numpy arrays
    :param X_batches: list of metadata entries describing image files
    :param T_batches: List of target class descriptions, numpy arrays
    :param pickling_dir:
    :return: No return
    '''
    for i in range(len(X_batches)):

        # Get the batches to export in this run
        X_batch = X_batches[i]
        # to be pickled
        T_cucumber = T_batches[i]

        # Parse the row to a dict, removes weird matlab format
        X_batch = matlab_to_dict(X_batch)

        parsed_tensors = []
        # Iterate through the dictionary's keys, which equal each photo's name
        for key in X_batch.keys():
            # Get the raw image using the key as a file name
            raw_image = tf.io.read_file(path_to_cars_train + key)

            # Decode that image as a jpeg
            jpeg_image = tf.io.decode_jpeg(raw_image, name=key.split('.')[0])
            del raw_image
            # crop the image to the car
            jpeg_image = crop(jpeg_image, X_batch[key])

            # pad it to the average h and w from above
            jpeg_image = tf.image.resize_with_pad(jpeg_image, height, width, antialias=True)

            # Add to the tensor list
            parsed_tensors.append(jpeg_image)

        print("Parsed {} tensors from batch {}".format(len(parsed_tensors), i))

        # make an X numpy array with the dims required to fit the tensors
        X_cucumber = np.ones((len(X_batch), height, width, 3), dtype=np.uint8)

        # Write out all the tensors to a np array
        for j in range(X_cucumber.shape[0]):
            X_cucumber[j] = parsed_tensors[j].numpy().astype(np.uint8)  # <--small, 0-255 which is perfect for jpg

        # Clear up space in memory
        for tensor in parsed_tensors:
            del tensor
        del parsed_tensors

        # Pickle the cucumbers
        pkl.dump(X_cucumber, open(pickling_dir + "batch" + str(i) + ".pkl", "wb"))
        pkl.dump(T_cucumber, open(pickling_dir + "batch" + str(i) + "_targets.pkl", "wb"))
