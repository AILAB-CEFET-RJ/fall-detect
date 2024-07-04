import pandas as pd
import os
import math
import numpy as np

'''
Checks if the directory exists, if not, creates the directory
'''
def create_directory_if_does_not_exist(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

'''
Organizes the list of dataset subdirectories 
in ascending order (Ex: ID1,ID2,ID3 ... ID15).
'''
def sort_by_number(id):
    return int(id[2:])

'''
Gets the path to access the sampling, acceleration
 and angular acceleration files of the dataset
 '''
def get_file_path(main_directory, subdirectory, position,preprocessing = None):
    subdirectory_path = os.path.join(main_directory, subdirectory)
    subdirectory_path_of_subdirectory = os.path.join(subdirectory_path, position)

    file_name = f'{subdirectory}_{position}_acceleration.csv'
    file_name_2 = f'{subdirectory}_{position}_sampling.csv'
    file_name_3 = f'{subdirectory}_{position}_angular_speed.csv'

    sampling_file = os.path.join(subdirectory_path_of_subdirectory, file_name_2)
    acc_file = os.path.join(subdirectory_path_of_subdirectory, file_name)
    gyr_file = os.path.join(subdirectory_path_of_subdirectory, file_name_3)

    if preprocessing == "sim":
        return acc_file,gyr_file,sampling_file,file_name,file_name_2,file_name_3
    return acc_file, gyr_file, sampling_file


'''
Adds the magnitude column {force resulting 
from the (a,w)x, (a,w)y and (a,w)z axes} in the dataframe.
'''
def add_magnitude_column(dataframe, sensor = None):
    initial_letter = None

    if sensor == "acc":
        initial_letter = "a"
    else:
        initial_letter = "w"

    resultant_force = []
    i = 0

    while i < len(dataframe[f'{initial_letter}x']):
        resultant = math.sqrt((dataframe[f'{initial_letter}x'][i]) ** 2 + (dataframe[f'{initial_letter}y'][i]) ** 2 + (dataframe[f'{initial_letter}z'][i]) ** 2)
        resultant_force.append(resultant)
        i += 1
    dataframe.insert(5, "Magnitude", resultant_force, True)

'''
Creates a data frame from each data file in the dataset.
'''
def create_dataframe(acc_file, gyr_file, sampling_file):

    acc_dataframe = pd.DataFrame(pd.read_csv(acc_file))
    gyr_dataframe= pd.DataFrame(pd.read_csv(gyr_file))
    sampling_dataframe = pd.DataFrame(pd.read_csv(sampling_file))

    add_magnitude_column(acc_dataframe, "acc")
    add_magnitude_column(gyr_dataframe)

    return acc_dataframe,gyr_dataframe,sampling_dataframe

'''
Apply the fourier transform to data arrays
'''
def fourier_transform(time_series):
    altered_time_series = []
    mean_time_series = np.mean(time_series)

    for i in time_series:
        #Subtraction from the average to Remove the DC Component (Zero Frequency Component).
        data = i - mean_time_series
        altered_time_series.append(data)
    altered_time_series = np.array(altered_time_series)

    return np.abs(np.fft.fft(altered_time_series))

'''
selects the data columns (a,w)x, (a,w)y, (a,w)z and mag
(gyr,acc) of the dataframe according to the index I of the
for loop that represents the access key for the file for 
each volunteer (ID1, ID2, etc.) and according to the activity
(ADL_1, ADL_2, etc.). Removes the value referring to the 
first observation of each activity, aiming to minimize 
any error in data collection.
'''
def section_data_array(acc_dataframe, gyr_dataframe, i,use_in_media_generator = None):
    magacc = acc_dataframe.loc[acc_dataframe["sampling"] == i, "Magnitude"]
    magacc = magacc.reset_index(drop=True)

    xacc = acc_dataframe.loc[acc_dataframe["sampling"] == i, "ax"]
    xacc = xacc.reset_index(drop=True)

    yacc = acc_dataframe.loc[acc_dataframe["sampling"] == i, "ay"]
    yacc = yacc.reset_index(drop=True)

    zacc = acc_dataframe.loc[acc_dataframe["sampling"] == i, "az"]
    zacc = zacc.reset_index(drop=True)

    maggyr = gyr_dataframe.loc[gyr_dataframe["sampling"] == i, "Magnitude"]
    maggyr = maggyr.reset_index(drop=True)

    xgyr = gyr_dataframe.loc[gyr_dataframe["sampling"] == i, "wx"]
    xgyr = xgyr.reset_index(drop=True)

    ygyr = gyr_dataframe.loc[gyr_dataframe["sampling"] == i, "wy"]
    ygyr = ygyr.reset_index(drop=True)

    zgyr = gyr_dataframe.loc[gyr_dataframe["sampling"] == i, "wz"]
    zgyr = zgyr.reset_index(drop=True)

    timestamp_acc = acc_dataframe.loc[acc_dataframe["sampling"] == i, "timestamp"]
    timestamp_acc = timestamp_acc.reset_index(drop=True)
    timestamp_acc = timestamp_acc.drop(0)
    timestamp_acc = timestamp_acc.reset_index(drop=True)

    timestamp_gyr = gyr_dataframe.loc[gyr_dataframe["sampling"] == i, "timestamp"]
    timestamp_gyr = timestamp_gyr.reset_index(drop=True)
    timestamp_gyr = timestamp_gyr.drop(0)
    timestamp_gyr = timestamp_gyr.reset_index(drop=True)

    if use_in_media_generator == "yes":
        return timestamp_acc, timestamp_gyr, magacc, xacc, yacc, zacc, maggyr, xgyr, ygyr, zgyr
    return magacc, xacc, yacc, zacc, maggyr, xgyr, ygyr, zgyr
'''
Adds data arrays formatted in the size of observations equivalent to five seconds 
(480 observations for the right and left wrist and 1050 observations for the chest) 
in the time domain and frequency domain lists.
'''
def add_data_arrays_to_time_and_frequency_data_lists(initial_index,final_index,array_size,data_array,data_array_list,fourier_transformed_data_array_list):
    data_array = data_array[initial_index:final_index]
    numpy_data_array = np.array(data_array)
    numpy_data_array = np.expand_dims(numpy_data_array, axis=1)
    data_array_list.append(numpy_data_array)

    transformed_data_array = fourier_transform(data_array)
    transformed_data_array = transformed_data_array[:int(array_size / 2)]
    numpy_transformed_data_array = np.array(transformed_data_array)
    numpy_transformed_data_array = np.expand_dims(numpy_transformed_data_array, axis=1)
    fourier_transformed_data_array_list.append(numpy_transformed_data_array)


'''
Returns the activity label for the four approaches.
'''
def create_labels(activity):

    #Multiple_classes_labels_1 represents the approach where each activity, whether performed with or without a rifle,
    # receives a distinct label. With the exception of activities FALL_5 and FALL_6, which receive a single label and
    # are considered only as lateral falls regardless of the fall position. The same applies to FALL_5_with_rifle and FALL_6_with_rifle.
    multiple_classes_labels_1 = {"ADL_1": 0, "ADL_2": 1, "ADL_3": 2, "ADL_4": 3, "ADL_5": 4, "ADL_6": 5, "ADL_7": 6, "ADL_8": 7,
                               "ADL_11": 8, "ADL_12": 9, "ADL_13": 10, "ADL_14": 11, "ADL_15": 12, "OM_1": 13, "OM_2": 14,
                               "OM_3": 15, "OM_4": 16, "OM_5": 17, "OM_6": 18, "OM_7": 19, "OM_8": 20, "OM_9": 21,
                               "FALL_1": 22, "FALL_2": 23, "FALL_3": 24, "FALL_5": 25, "FALL_6": 25,"FALL_1_with_rifle": 26,
                               "FALL_3_with_rifle": 27, "FALL_5_with_rifle": 28, "FALL_6_with_rifle": 28,"ADL_1_with_rifle": 29,
                               "ADL_4_with_rifle": 30, "ADL_5_with_rifle": 31, "ADL_6_with_rifle": 32,"ADL_11_with_rifle": 33,
                               "ADL_12_with_rifle": 34, "ADL_13_with_rifle": 35, "ADL_14_with_rifle": 36}


    #Multiple_classes_labels_2 represents the approach in which each activity performed, regardless of whether a rifle
    # was used or not, receives a label according to the activity. For example, activity ADL_1 receives the label 0 and
    # encompasses standing activities recorded with and without the use of a rifle. The exception is activities FALL_5
    # and FALL_6, which receive a single label and are considered only as a lateral fall, regardless of the fall position.
    multiple_classes_labels_2 = {"ADL_1": 0, "ADL_2": 1, "ADL_3": 2, "ADL_4": 3, "ADL_5": 4, "ADL_6": 5, "ADL_7": 6,
                               "ADL_8": 7,"ADL_11": 8, "ADL_12": 9, "ADL_13": 10, "ADL_14": 11, "ADL_15": 12, "OM_1": 13,
                               "OM_2": 14,"OM_3": 15, "OM_4": 16, "OM_5": 17, "OM_6": 18, "OM_7": 19, "OM_8": 20, "OM_9": 21,
                               "FALL_1": 22, "FALL_2": 23, "FALL_3": 24, "FALL_5": 25, "FALL_6": 25}

    # binary_classes_labels_1 is the approach where all activities of daily living and military operations receive
    # label and falls receive label 0. However, activities 0M6 to OM8 relating to the transition to the prone
    # firing position are considered as falling activities.
    binary_classes_labels_1 = {"ADL_1": 1, "ADL_2": 1, "ADL_3": 1, "ADL_4": 1, "ADL_5": 1, "ADL_6": 1, "ADL_7": 1, "ADL_8": 1,
                       "ADL_11": 1, "ADL_12": 1, "ADL_13": 1, "ADL_14": 1, "ADL_15": 1, "OM_1": 1,
                       "OM_2": 1, "OM_3": 1, "OM_4": 1, "OM_5": 1, "OM_6": 0, "OM_7": 0, "OM_8": 0, "OM_9": 1,
                       "FALL_1": 0, "FALL_2": 0, "FALL_3": 0, "FALL_5": 0, "FALL_6": 0}

    #binary_classes_labels_2 is the approach where all activities of daily living and military operations receive
    # label 1 and falls receive label 0. However, activities 0M6 to OM8 relating to the transition to the prone
    # shooting position are not considered as fall activities and receive label 1.
    binary_classes_labels_2 = {"ADL_1": 1, "ADL_2": 1, "ADL_3": 1, "ADL_4": 1, "ADL_5": 1, "ADL_6": 1, "ADL_7": 1, "ADL_8": 1,
                       "ADL_11": 1, "ADL_12": 1, "ADL_13": 1, "ADL_14": 1, "ADL_15": 1, "OM_1": 1,
                       "OM_2": 1, "OM_3": 1, "OM_4": 1, "OM_5": 1, "OM_6": 1, "OM_7": 1, "OM_8": 1, "OM_9": 1,
                       "FALL_1": 0, "FALL_2": 0, "FALL_3": 0, "FALL_5": 0, "FALL_6": 0}

    activity_without_rifle = activity.split("_with_rifle")[0]

    multiple_class_label_1 = multiple_classes_labels_1.get(activity)
    multiple_class_label_2 = multiple_classes_labels_2.get(activity_without_rifle)
    binary_class_label_1 = binary_classes_labels_1.get(activity_without_rifle)
    binary_class_label_2 = binary_classes_labels_2.get(activity_without_rifle)

    return multiple_class_label_1,multiple_class_label_2,binary_class_label_1,binary_class_label_2

'''
Add the labels to the accelerometer and gyroscope label lists.
'''
def add_labels(multiple_class_label_1, multiple_class_label_2, binary_class_label_1, binary_class_label_2, labels_list):

    labels_list[0].append(multiple_class_label_1)
    labels_list[1].append(multiple_class_label_2)
    labels_list[2].append(binary_class_label_1)
    labels_list[3].append(binary_class_label_2)

