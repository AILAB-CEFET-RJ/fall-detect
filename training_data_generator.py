import argparse
import os
from builders.data_training_builders import (sort_by_number,get_file_path,create_dataframe,create_directory_if_does_not_exist)
from builders.data_training_generators import generate_activities
import numpy as np


''' EXECUTION OF THE TRAINING DATA GENERATION PROGRAM '''

parser = argparse.ArgumentParser(description="Script for generating training data")
parser.add_argument('position', type=str, choices=['chest', 'left', 'right'], help='Sensor position')
args = parser.parse_args()

position = args.position.upper()

current_directory = os.path.dirname(__file__)

main_directory = os.path.join(current_directory, 'database')

subdirectory_list = os.listdir(main_directory)

subdirectory_list.sort(key=sort_by_number)

if position == "CHEST":

    label_directory = os.path.join(current_directory, 'labels_and_data','labels','chest')
    data_array_directory = os.path.join(current_directory, 'labels_and_data','data','chest')

    create_directory_if_does_not_exist(label_directory)
    create_directory_if_does_not_exist(data_array_directory)

elif position == "LEFT":

    label_directory = os.path.join(current_directory, 'labels_and_data', 'labels', 'left')
    data_array_directory = os.path.join(current_directory, 'labels_and_data', 'data', 'left')

    create_directory_if_does_not_exist(label_directory)
    create_directory_if_does_not_exist(data_array_directory)
else:
    label_directory = os.path.join(current_directory, 'labels_and_data', 'labels', 'right')
    data_array_directory = os.path.join(current_directory, 'labels_and_data', 'data', 'right')

    create_directory_if_does_not_exist(label_directory)
    create_directory_if_does_not_exist(data_array_directory)


list_of_data_arrays_in_the_time_domain = [[] for _ in range(8)]

list_of_data_arrays_in_the_frequency_domain = [[] for _ in range(8)]

labels_list = [[] for _ in range(4)]

print("comparação realizada")
for subdirectory in subdirectory_list:
    acc,gyr,sampling = get_file_path(main_directory, subdirectory, position)
    acc_dataframe, gyr_dataframe, sampling_dataframe = create_dataframe(acc, gyr, sampling)
    generate_activities(acc_dataframe, gyr_dataframe, sampling_dataframe, position,
                        list_of_data_arrays_in_the_time_domain, list_of_data_arrays_in_the_frequency_domain,
                        labels_list)

np.save(os.path.join(label_directory, 'multiple_class_label_1.npy'), np.asarray(labels_list[0]))
np.save(os.path.join(label_directory, 'multiple_class_label_2.npy'), np.asarray(labels_list[1]))
np.save(os.path.join(label_directory, 'binary_class_label_1.npy'), np.asarray(labels_list[2]))
np.save(os.path.join(label_directory, 'binary_class_label_2.npy'), np.asarray(labels_list[3]))

np.save(os.path.join(data_array_directory, 'magacc_time_domain_data_array.npy'), np.asarray(list_of_data_arrays_in_the_time_domain[0]))
np.save(os.path.join(data_array_directory, 'magacc_frequency_domain_data_array.npy'), np.asarray(list_of_data_arrays_in_the_frequency_domain[0]))

np.save(os.path.join(data_array_directory, 'acc_x_y_z_axes_time_domain_data_array.npy'),
        np.concatenate((np.asarray(list_of_data_arrays_in_the_time_domain[1]), np.asarray(list_of_data_arrays_in_the_time_domain[2]),
                        np.asarray(list_of_data_arrays_in_the_time_domain[3])), axis=2))

np.save(os.path.join(data_array_directory, 'acc_x_y_z_axes_frequency_domain_data_array.npy'),
        np.concatenate((np.asarray(list_of_data_arrays_in_the_frequency_domain[1]), np.asarray(list_of_data_arrays_in_the_frequency_domain[2]),
                        np.asarray(list_of_data_arrays_in_the_frequency_domain[3])), axis=2))

np.save(os.path.join(data_array_directory, 'maggyr_time_domain_data_array.npy'), np.asarray(list_of_data_arrays_in_the_time_domain[4]))
np.save(os.path.join(data_array_directory, 'maggyr_frequency_domain_data_array.npy'), np.asarray(list_of_data_arrays_in_the_frequency_domain[4]))

np.save(os.path.join(data_array_directory, 'gyr_x_y_z_axes_time_domain_data_array.npy'),
        np.concatenate((np.asarray(list_of_data_arrays_in_the_time_domain[5]), np.asarray(list_of_data_arrays_in_the_time_domain[6]),
                        np.asarray(list_of_data_arrays_in_the_time_domain[7])), axis=2))

np.save(os.path.join(data_array_directory, 'gyr_x_y_z_axes_frequency_domain_data_array.npy'),
        np.concatenate((np.asarray(list_of_data_arrays_in_the_frequency_domain[5]), np.asarray(list_of_data_arrays_in_the_frequency_domain[6]),
                        np.asarray(list_of_data_arrays_in_the_frequency_domain[7])), axis=2))

np.save(os.path.join(data_array_directory, 'magacc_and_maggyr_time_domain_data_array.npy'),
        np.concatenate((np.asarray(list_of_data_arrays_in_the_time_domain[0]), np.asarray(list_of_data_arrays_in_the_time_domain[4])), axis=2))

np.save(os.path.join(data_array_directory, 'magacc_and_maggyr_frequency_domain_data_array.npy'),
        np.concatenate((np.asarray(list_of_data_arrays_in_the_frequency_domain[0]), np.asarray(list_of_data_arrays_in_the_frequency_domain[4])), axis=2))

np.save(os.path.join(data_array_directory, 'acc_and_gyr_three_axes_time_domain_data_array.npy'),
        np.concatenate((np.asarray(list_of_data_arrays_in_the_time_domain[1]),np.asarray(list_of_data_arrays_in_the_time_domain[2]),
                        np.asarray(list_of_data_arrays_in_the_time_domain[3]),np.asarray(list_of_data_arrays_in_the_time_domain[5]),
                        np.asarray(list_of_data_arrays_in_the_time_domain[6]),np.asarray(list_of_data_arrays_in_the_time_domain[7])), axis=2))

np.save(os.path.join(data_array_directory, 'acc_and_gyr_three_axes_frequency_domain_data_array.npy'),
        np.concatenate((np.asarray(list_of_data_arrays_in_the_frequency_domain[1]), np.asarray(list_of_data_arrays_in_the_frequency_domain[2]),
                        np.asarray(list_of_data_arrays_in_the_frequency_domain[3]),np.asarray(list_of_data_arrays_in_the_frequency_domain[5]),
                        np.asarray(list_of_data_arrays_in_the_frequency_domain[6]),np.asarray(list_of_data_arrays_in_the_frequency_domain[7])), axis=2))
