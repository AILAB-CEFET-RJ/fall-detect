import os
import statistics

from builders.data_training_builders import sort_by_number,get_file_path,create_dataframe, section_data_array

'''Generates an array of times in seconds from the timestamps.'''
def generate_time_array_in_seconds(timesatamp, timestamp_list):
    for i in range(len(timesatamp)):
        first_timestamp = timesatamp[0]
        if i != len(timesatamp) - 1:
            time_in_seconds = ((timesatamp[i + 1] - first_timestamp) / 1000)
            timestamp_list.append(time_in_seconds)

'''Calculates the number of observations for each 5-second interval and stores 
them in the observations list, which represents the number of observations for 
each interval.'''
def calculate_number_of_observations(array_in_seconds,quantity_observations_list):
    interval = 5
    current_time = 0
    initial_index = 0

    for i in range(len(array_in_seconds)):

        if array_in_seconds[i] >= current_time + interval:
            final_index = i

            quantity_observations = len(array_in_seconds[initial_index:final_index])
            quantity_observations_list.append(quantity_observations)
            current_time += interval
            initial_index = final_index

'''Calculates the mean and standard deviation of the observations stored in 
the observations list.'''
def calculate_median_and_std(quantity_observations_list):
    median = statistics.mean(quantity_observations_list)
    std = statistics.stdev(quantity_observations_list)

    return median,std

'''selects the timestamp from the data file for each activity and 
execute the functions generate_time_array_in_seconds and calculate_number_of_observations
 for both the accelerometer and gyroscope sensors'''
def generate_activities(acc_dataframe, gyr_dataframe, sampling_dataframe):

    for i in (sampling_dataframe["id"]):

        timestamp_acc,timestamp_gyr,magacc,xacc,yacc,zacc,maggyr,xgyr,ygyr,zgyr = section_data_array(acc_dataframe, gyr_dataframe, i,"yes")

        acc_time_in_seconds = [0,]
        gyr_time_in_seconds = [0,]

        generate_time_array_in_seconds(timestamp_acc, acc_time_in_seconds)
        generate_time_array_in_seconds(timestamp_gyr, gyr_time_in_seconds)

        calculate_number_of_observations(acc_time_in_seconds,acc_quantity_observations)
        calculate_number_of_observations(gyr_time_in_seconds,gyr_quantity_observations )

''' PROGRAM EXECUTION '''

def run_observation_median_program(position):

    subdirectory_list = os.listdir(main_directory)
    subdirectory_list.sort(key=sort_by_number)

    for subdirectory in subdirectory_list:
        acc,gyr,sampling = get_file_path(main_directory, subdirectory, position)
        acc_dataframe, gyr_dataframe, sampling_dataframe = create_dataframe(acc, gyr, sampling)
        generate_activities(acc_dataframe, gyr_dataframe, sampling_dataframe)

    acc_median,acc_std = calculate_median_and_std(acc_quantity_observations)
    gyr_median,gyr_std = calculate_median_and_std(gyr_quantity_observations)

    result_acc = f'{position}_acc_median = {acc_median}, {position}_acc_std = {acc_std}'
    result_gyr = f'{position}_gyr_median = {gyr_median}, {position}_gyr_std = {gyr_std}'

    print(result_acc)
    print(result_gyr)

    results.append(result_acc)
    results.append(result_gyr)


    acc_quantity_observations.clear()
    gyr_quantity_observations.clear()

def save_results_to_file():
    results_directory = os.path.join(os.path.dirname(__file__), 'observation_median_results')
    os.makedirs(results_directory, exist_ok=True)
    results_file_path = os.path.join(results_directory, 'results.txt')
    with open(results_file_path, 'w') as file:
        for result in results:
            file.write(result)

main_directory =  os.path.join(os.path.dirname(__file__),'database')
acc_quantity_observations = []
gyr_quantity_observations = []
results = []

positions = ["LEFT", "RIGHT", "CHEST"]
for position in positions:
    run_observation_median_program(position)

save_results_to_file()
