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
def get_file_path(main_directory, subdirectory, position):
    subdirectory_path = os.path.join(main_directory, subdirectory)
    subdirectory_path_of_subdirectory = os.path.join(subdirectory_path, position)

    file_name = f'{subdirectory}_{position}_acceleration.csv'
    file_name_2 = f'{subdirectory}_{position}_sampling.csv'
    file_name_3 = f'{subdirectory}_{position}_angular_speed.csv'

    sampling_file = os.path.join(subdirectory_path_of_subdirectory, file_name_2)
    acc_file = os.path.join(subdirectory_path_of_subdirectory, file_name)
    gyr_file = os.path.join(subdirectory_path_of_subdirectory, file_name_3)

    return acc_file,gyr_file,sampling_file

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
def section_data_array(acc_dataframe, gyr_dataframe, i):
    magacc = acc_dataframe.loc[acc_dataframe["sampling"] == i, "Magnitude"]
    magacc = magacc.reset_index(drop=True)
    magacc = magacc.drop(0)

    xacc = acc_dataframe.loc[acc_dataframe["sampling"] == i, "ax"]
    xacc = xacc.reset_index(drop=True)
    xacc = xacc.drop(0)

    yacc = acc_dataframe.loc[acc_dataframe["sampling"] == i, "ay"]
    yacc = yacc.reset_index(drop=True)
    yacc = yacc.drop(0)

    zacc = acc_dataframe.loc[acc_dataframe["sampling"] == i, "az"]
    zacc = zacc.reset_index(drop=True)
    zacc = zacc.drop(0)

    maggyr = gyr_dataframe.loc[gyr_dataframe["sampling"] == i, "Magnitude"]
    maggyr = maggyr.reset_index(drop=True)
    maggyr = maggyr.drop(0)

    xgyr = gyr_dataframe.loc[gyr_dataframe["sampling"] == i, "wx"]
    xgyr = xgyr.reset_index(drop=True)
    xgyr = xgyr.drop(0)

    ygyr = gyr_dataframe.loc[gyr_dataframe["sampling"] == i, "wy"]
    ygyr = ygyr.reset_index(drop=True)
    ygyr = ygyr.drop(0)

    zgyr = gyr_dataframe.loc[gyr_dataframe["sampling"] == i, "wz"]
    zgyr = zgyr.reset_index(drop=True)
    zgyr = zgyr.drop(0)

    return magacc,xacc,yacc,zacc,maggyr,xgyr,ygyr,zgyr

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
    #Multiple_classes_labels represents the approach in which each activity performed by volunteers receives a
    #distinct label, which did not apply to the activities FALL_5 and FALL_6 which received the same label
    #because they are lateral falls (left and right).
    multiple_classes_labels = {"ADL_1": 0, "ADL_2": 1, "ADL_3": 2, "ADL_4": 3, "ADL_5": 4, "ADL_6": 5, "ADL_7": 6, "ADL_8": 7,
                        "ADL_11": 8, "ADL_12": 9, "ADL_13": 10, "ADL_14": 11, "ADL_15": 12, "OM_1": 13, "OM_2": 14,
                        "OM_3": 15, "OM_4": 16, "OM_5": 17, "OM_6": 18, "OM_7": 19, "OM_8": 20, "OM_9": 21,
                        "FALL_1": 22, "FALL_2": 23, "FALL_3": 24, "FALL_5": 25, "FALL_6": 25}

    #three_classes_labels is an approach where labels are defined for the following classes: Activities of
    # Daily Living, Military Operations and Falls.
    three_classes_labels = {"ADL_1": 1, "ADL_2": 1, "ADL_3": 1, "ADL_4": 1, "ADL_5": 1, "ADL_6": 1, "ADL_7": 1, "ADL_8": 1,
                   "ADL_11": 1, "ADL_12": 1, "ADL_13": 1, "ADL_14": 1, "ADL_15": 1, "OM_1": 2,
                   "OM_2": 2, "OM_3": 2, "OM_4": 2, "OM_5": 2, "OM_6": 2, "OM_7": 2, "OM_8": 2, "OM_9": 2,
                   "FALL_1": 0, "FALL_2": 0, "FALL_3": 0, "FALL_5": 0, "FALL_6": 0}

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
                       "OM_2": 1, "OM_3": 1, "OM_4": 1, "OM_5": 1, "OM_6": 0, "OM_7": 0, "OM_8": 0, "OM_9": 1,
                       "FALL_1": 0, "FALL_2": 0, "FALL_3": 0, "FALL_5": 0, "FALL_6": 0}

    multiple_class_label = multiple_classes_labels.get(activity)
    three_class_label = three_classes_labels.get(activity)
    binary_class_label_1 = binary_classes_labels_1.get(activity)
    binary_class_label_2 = binary_classes_labels_2.get(activity)

    return multiple_class_label,three_class_label,binary_class_label_1,binary_class_label_2

'''
Add the labels to the accelerometer and gyroscope label lists.
'''
def add_labels(multiple_class_label,three_class_label,binary_class_label_1,binary_class_label_2,data_array_generator = None,add_labels_in_lista = None ):

    if data_array_generator == "other":
        if add_labels_in_lista == "yes_acc":

            accelerometer_multiple_class_label_list.append(multiple_class_label)
            accelerometer_three_class_label_list.append(three_class_label)
            accelerometer_binary_class_label_1_list.append(binary_class_label_1)
            accelerometer_binary_class_label_2_list.append(binary_class_label_2)

        elif add_labels_in_lista == "yes_gir":

            gyroscope_multiple_class_label_list.append(multiple_class_label)
            gyroscope_three_class_label_list.append(three_class_label)
            gyroscope_binary_class_label_1_list.append(binary_class_label_1)
            gyroscope_binary_class_label_2_list.append(binary_class_label_2)
    else:

        accelerometer_multiple_class_label_list.append(multiple_class_label)
        accelerometer_three_class_label_list.append(three_class_label)
        accelerometer_binary_class_label_1_list.append(binary_class_label_1)
        accelerometer_binary_class_label_2_list.append(binary_class_label_2)
        gyroscope_multiple_class_label_list.append(multiple_class_label)
        gyroscope_three_class_label_list.append(three_class_label)
        gyroscope_binary_class_label_1_list.append(binary_class_label_1)
        gyroscope_binary_class_label_2_list.append(binary_class_label_2)

'''
Transforms the activities "FALL_1", "FALL_2", "FALL_3", "FALL_5", "FALL_6", "ADL_7", "ADL_8" and "ADL_15" 
into five-second arrays and adds them to the time domain and data domain lists. frequency.   Falling 
activities originally last 10 seconds, however the fall itself occurs within the first five seconds. 
Activities ADL_7" and "ADL_8" last 6 seconds, so the last second is being discarded. It was found that 
"ADL_15" also occurs in the first 5 seconds, so we discard observations after this time.
'''
def generate_array_of_activities_lasting_5seconds(data_array, array_size, data_array_list, fourier_transformed_data_array_list):
    add_data_arrays_to_time_and_frequency_data_lists(0, array_size, array_size, data_array, data_array_list, fourier_transformed_data_array_list)

'''
It transforms activities in which state transitions occur (for example: transition from walking to the lying 
shooting position into an array of size equivalent to 5 seconds. The function maps the largest force peak that 
occurs during the activity and moves the start and the end of the data array as a function of this peak.
'''
def generate_array_of_transition_activities(data_array, array_size, data_array_list, fourier_transformed_data_array_list):
    maximum_value = max(data_array)
    index_of_maximum_value = int(data_array.loc[data_array == maximum_value].index[0])
    initial_index = int(index_of_maximum_value - (array_size / 2))
    final_index = int(index_of_maximum_value + (array_size / 2))

    if initial_index < 0:
        initial_index = 0
        final_index = array_size
    elif final_index > int(data_array.index[-1]):
        final_index = int(data_array.index[-1])
        initial_index = final_index - array_size

    add_data_arrays_to_time_and_frequency_data_lists(initial_index,final_index, array_size, data_array, data_array_list,fourier_transformed_data_array_list)

'''
Transforms other activities lasting more than 10 seconds into several data arrays with a size of 5 seconds.
For example, the ADL_3 activity that lasts 30 seconds turns into 6 arrays of 5 seconds (480 observations or
1050 observations).
'''
def generate_array_of_other_activities(data_array, array_size, data_array_list, fourier_transformed_data_array_list, multiple_class_label, three_class_label, binary_class_label_1, binary_class_label_2,generate_labels = None, add_labels_in_lista = None):
    parts = math.floor(len(data_array) / array_size)
    initial_index = 0
    final_index = array_size

    for i in range(parts):
        add_data_arrays_to_time_and_frequency_data_lists(initial_index,final_index, array_size, data_array,data_array_list,fourier_transformed_data_array_list)

        if generate_labels == "yes":
            add_labels(multiple_class_label, three_class_label, binary_class_label_1, binary_class_label_2,"other", add_labels_in_lista)

        initial_index += array_size
        final_index += array_size

"""
Populates the lists with data arrays and labels for each activity for all 
collected data files. Used inside a "for" loop in the "generate_activities" function.
"""
def create_data_sets_for_training(position, activity, magacc, xacc, yacc, zacc, maggyr, xgyr, ygyr, zgyr):

    five_second_activity_list = ["FALL_1", "FALL_2","FALL_3","FALL_5","FALL_6","ADL_7","ADL_8","ADL_15"]
    transition_activities_list = ["OM_3", "OM_4", "OM_5","OM_6", "OM_7", "OM_8"]

    multiple_class_label,three_class_label,binary_class_label_1,binary_class_label_2 = create_labels(activity)

    array_size = 1050 if position == "CHEST" else 480

    if len(xgyr) >= array_size and len(xacc) >= array_size:
        if activity in five_second_activity_list:

            generate_array_of_activities_lasting_5seconds(magacc, array_size, magacc_data_array_list,magacc_transformed_data_array_list)
            generate_array_of_activities_lasting_5seconds(xacc, array_size, xacc_data_array_list,xacc_transformed_data_array_list)
            generate_array_of_activities_lasting_5seconds(yacc, array_size, yacc_data_array_list,yacc_transformed_data_array_list)
            generate_array_of_activities_lasting_5seconds(zacc, array_size, zacc_data_array_list,zacc_transformed_data_array_list)
            generate_array_of_activities_lasting_5seconds(maggyr, array_size, maggyr_data_array_list, maggyr_transformed_data_array_list)
            generate_array_of_activities_lasting_5seconds(xgyr, array_size, xgyr_data_array_list, xgyr_transformed_data_array_list)
            generate_array_of_activities_lasting_5seconds(ygyr, array_size, ygyr_data_array_list, ygyr_transformed_data_array_list)
            generate_array_of_activities_lasting_5seconds(zgyr, array_size, zgyr_data_array_list, zgyr_transformed_data_array_list)

            add_labels(multiple_class_label, three_class_label, binary_class_label_1, binary_class_label_2)

        elif activity in transition_activities_list:
            generate_array_of_transition_activities(magacc, array_size, magacc_data_array_list,magacc_transformed_data_array_list)
            generate_array_of_transition_activities(xacc, array_size, xacc_data_array_list,xacc_transformed_data_array_list)
            generate_array_of_transition_activities(yacc, array_size, yacc_data_array_list,yacc_transformed_data_array_list)
            generate_array_of_transition_activities(zacc, array_size, zacc_data_array_list,zacc_transformed_data_array_list)
            generate_array_of_transition_activities(maggyr, array_size, maggyr_data_array_list, maggyr_transformed_data_array_list)
            generate_array_of_transition_activities(xgyr, array_size, xgyr_data_array_list, xgyr_transformed_data_array_list)
            generate_array_of_transition_activities(ygyr, array_size, ygyr_data_array_list, ygyr_transformed_data_array_list)
            generate_array_of_transition_activities(zgyr, array_size, zgyr_data_array_list, zgyr_transformed_data_array_list)

            add_labels(multiple_class_label,three_class_label,binary_class_label_1,binary_class_label_2)
        else:
            generate_array_of_other_activities(magacc, array_size, magacc_data_array_list, magacc_transformed_data_array_list, multiple_class_label, three_class_label, binary_class_label_1, binary_class_label_2,"yes","yes_acc")
            generate_array_of_other_activities(xacc, array_size, xacc_data_array_list, xacc_transformed_data_array_list, multiple_class_label, three_class_label, binary_class_label_1, binary_class_label_2)
            generate_array_of_other_activities(yacc, array_size, yacc_data_array_list, yacc_transformed_data_array_list, multiple_class_label, three_class_label, binary_class_label_1, binary_class_label_2)
            generate_array_of_other_activities(zacc, array_size, zacc_data_array_list, zacc_transformed_data_array_list, multiple_class_label, three_class_label, binary_class_label_1, binary_class_label_2)
            generate_array_of_other_activities(maggyr, array_size, maggyr_data_array_list, maggyr_transformed_data_array_list, multiple_class_label, three_class_label, binary_class_label_1, binary_class_label_2, "yes", "yes_gir")
            generate_array_of_other_activities(xgyr, array_size, xgyr_data_array_list, xgyr_transformed_data_array_list, multiple_class_label, three_class_label, binary_class_label_1, binary_class_label_2)
            generate_array_of_other_activities(ygyr, array_size, ygyr_data_array_list, ygyr_transformed_data_array_list, multiple_class_label, three_class_label, binary_class_label_1, binary_class_label_2)
            generate_array_of_other_activities(zgyr, array_size, zgyr_data_array_list, zgyr_transformed_data_array_list, multiple_class_label, three_class_label, binary_class_label_1, binary_class_label_2)

'''
Populates the lists with data arrays and labels for each activity 
'''
def generate_activities(acc_dataframe, gyr_dataframe, sampling_dataframe):

    for i in (sampling_dataframe["id"]):

        activity = (sampling_dataframe.loc[sampling_dataframe["id"] == i, "exercise"].iloc[0])

        magacc,xacc,yacc,zacc,maggyr,xgyr,ygyr,zgyr = section_data_array(acc_dataframe, gyr_dataframe, i)

        create_data_sets_for_training(position, activity, magacc, xacc, yacc, zacc, maggyr,xgyr,ygyr,zgyr)


''' EXECUTION OF THE TRAINING DATA GENERATION PROGRAM '''

main_directory = "../database"

subdirectory_list = os.listdir(main_directory)

subdirectory_list.sort(key=sort_by_number)

input("Enter which position you want to generate the data for (CHEST, LEFT or RIGHT)")
position = input("").upper()

if position == "CHEST":

    label_directory = "../labels_and_data/labels/chest"
    data_array_directory = "../labels_and_data/data/chest"

    create_directory_if_does_not_exist(label_directory)
    create_directory_if_does_not_exist(data_array_directory)

elif position == "LEFT":

    label_directory = "../labels_and_data/labels/left"
    data_array_directory = "../labels_and_data/data/left"

    create_directory_if_does_not_exist(label_directory)
    create_directory_if_does_not_exist(data_array_directory)
else:
    label_directory = "../labels_and_data/labels/right"
    data_array_directory = "../labels_and_data/data/right"

    create_directory_if_does_not_exist(label_directory)
    create_directory_if_does_not_exist(data_array_directory)

#magacc
magacc_data_array_list = []
#xacc
xacc_data_array_list = []
#yacc
yacc_data_array_list = []
#zacc
zacc_data_array_list = []

#maggir
maggyr_data_array_list = []
#xgir
xgyr_data_array_list = []
#ygir
ygyr_data_array_list = []
#zgir
zgyr_data_array_list = []

#magacc in the frequency domain
magacc_transformed_data_array_list = []
#xacc in the frequency domain
xacc_transformed_data_array_list = []
#yacc in the frequency domain
yacc_transformed_data_array_list = []
#zacc in the frequency domain
zacc_transformed_data_array_list = []

#maggir in the frequency domain
maggyr_transformed_data_array_list = []
#xgir in the frequency domain
xgyr_transformed_data_array_list = []
#ygir in the frequency domain
ygyr_transformed_data_array_list= []
#zgir in the frequency domain
zgyr_transformed_data_array_list = []

accelerometer_multiple_class_label_list = []
accelerometer_three_class_label_list = []
accelerometer_binary_class_label_1_list = []
accelerometer_binary_class_label_2_list = []

gyroscope_multiple_class_label_list = []
gyroscope_three_class_label_list = []
gyroscope_binary_class_label_1_list = []
gyroscope_binary_class_label_2_list = []


for subdirectory in subdirectory_list:
    acc,gyr,sampling = get_file_path(main_directory, subdirectory, position)
    acc_dataframe, gyr_dataframe, sampling_dataframe = create_dataframe(acc, gyr, sampling)
    generate_activities(acc_dataframe, gyr_dataframe, sampling_dataframe)

np.save(os.path.join(label_directory, 'accelerometer_multiple_class_label.npy'), np.asarray(accelerometer_multiple_class_label_list))
np.save(os.path.join(label_directory, 'accelerometer_three_class_label.npy'), np.asarray(accelerometer_three_class_label_list))
np.save(os.path.join(label_directory, 'accelerometer_binary_class_label_1.npy'), np.asarray(accelerometer_binary_class_label_1_list))
np.save(os.path.join(label_directory, 'accelerometer_binary_class_label_2.npy'), np.asarray(accelerometer_binary_class_label_2_list))

np.save(os.path.join(label_directory, 'gyroscope_multiple_class_label.npy'), np.asarray(gyroscope_multiple_class_label_list))
np.save(os.path.join(label_directory, 'gyroscope_three_class_label.npy'), np.asarray(gyroscope_three_class_label_list))
np.save(os.path.join(label_directory, 'gyroscope_binary_class_label_1.npy'), np.asarray(gyroscope_binary_class_label_1_list))
np.save(os.path.join(label_directory, 'gyroscope_binary_class_label_2.npy'), np.asarray(gyroscope_binary_class_label_2_list))

np.save(os.path.join(data_array_directory, 'magacc_time_domain_data_array.npy'), np.asarray(magacc_data_array_list))
np.save(os.path.join(data_array_directory, 'magacc_frequency_domain_data_array.npy'), np.asarray(magacc_transformed_data_array_list))
np.save(os.path.join(data_array_directory, 'xacc_time_domain_data_array.npy'), np.asarray(xacc_data_array_list))
np.save(os.path.join(data_array_directory, 'xacc_frequency_domain_data_array.npy'), np.asarray(xacc_transformed_data_array_list))
np.save(os.path.join(data_array_directory, 'yacc_time_domain_data_array.npy'), np.asarray(yacc_data_array_list))
np.save(os.path.join(data_array_directory, 'yacc_frequency_domain_data_array.npy'), np.asarray(yacc_transformed_data_array_list))
np.save(os.path.join(data_array_directory, 'zacc_time_domain_data_array.npy'), np.asarray(zacc_data_array_list))
np.save(os.path.join(data_array_directory, 'zacc_frequency_domain_data_array.npy'), np.asarray(zacc_transformed_data_array_list))

np.save(os.path.join(data_array_directory, 'maggyr_time_domain_data_array.npy'), np.asarray(maggyr_data_array_list))
np.save(os.path.join(data_array_directory, 'maggyr_frequency_domain_data_array.npy'), np.asarray(maggyr_transformed_data_array_list))
np.save(os.path.join(data_array_directory, 'xgyr_time_domain_data_array.npy'), np.asarray(xgyr_data_array_list))
np.save(os.path.join(data_array_directory, 'xgyr_frequency_domain_data_array'), np.asarray(xgyr_transformed_data_array_list))
np.save(os.path.join(data_array_directory, 'ygyr_time_domain_data_array.npy'), np.asarray(ygyr_data_array_list))
np.save(os.path.join(data_array_directory, 'ygyr_frequency_domain_data_array.npy'), np.asarray(ygyr_transformed_data_array_list))
np.save(os.path.join(data_array_directory, 'zgyr_time_domain_data_array.npy'), np.asarray(zgyr_data_array_list))
np.save(os.path.join(data_array_directory, 'zgyr_frequency_domain_data_array'), np.asarray(zgyr_transformed_data_array_list))



