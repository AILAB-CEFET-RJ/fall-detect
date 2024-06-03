from ..training_data_generator.training_data_generator import sort_by_number,get_file_path,add_magnitude_column,section_data_array,create_dataframe
import os
import statistics

def generate_time_array_in_seconds(timesatamp, timestamp_list):
    for i in range(len(timesatamp)):
        first_timestamp = timesatamp[0]
        if i != len(timesatamp) - 1:
            time_in_seconds = ((timesatamp[i + 1] - first_timestamp) / 1000)
            timestamp_list.append(time_in_seconds)

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

def calculate_median_and_std(quantity_observations_list):
    median = statistics.mean(quantity_observations_list)
    std = statistics.stdev(quantity_observations_list)

    return median,std

def generate_activities(acc_dataframe, gyr_dataframe, sampling_dataframe):

    for i in (sampling_dataframe["id"]):

        timestamp_acc,timestamp_gyr,magacc,xacc,yacc,zacc,maggyr,xgyr,ygyr,zgyr = section_data_array(acc_dataframe, gyr_dataframe, i,"yes")

        acc_time_in_seconds = [0,]
        gyr_time_in_seconds = [0,]

        generate_time_array_in_seconds(timestamp_acc, acc_time_in_seconds)
        generate_time_array_in_seconds(timestamp_gyr, gyr_time_in_seconds)

        calculate_number_of_observations(acc_time_in_seconds,acc_quantity_observations)
        calculate_number_of_observations(gyr_time_in_seconds,gyr_quantity_observations )

def run_observation_median_program(position):

    subdirectory_list = os.listdir(main_directory)
    subdirectory_list.sort(key=sort_by_number)

    for subdirectory in subdirectory_list:
        acc,gyr,sampling = get_file_path(main_directory, subdirectory, position)
        acc_dataframe, gyr_dataframe, sampling_dataframe = create_dataframe(acc, gyr, sampling)
        generate_activities(acc_dataframe, gyr_dataframe, sampling_dataframe)

    acc_median,acc_std = calculate_median_and_std(acc_quantity_observations)
    gyr_median,gyr_std = calculate_median_and_std(gyr_quantity_observations)

    print(f'{position}_acc_median = {acc_median}, {position}_acc_std = {acc_std}')
    print(f'{position}_acc_median = {gyr_median}, {position}_acc_std = {gyr_std}')

    acc_quantity_observations.clear()
    gyr_quantity_observations.clear()

def save_results_to_file():
    results_directory = os.path.join(os.path.dirname(__file__), 'observation_median_results')
    os.makedirs(results_directory, exist_ok=True)
    results_file_path = os.path.join(results_directory, 'results.txt')
    with open(results_file_path, 'w') as file:
        for result in results:
            file.write(result)

main_directory = "../database"
acc_quantity_observations = []
gyr_quantity_observations = []
results = []

positions = ["LEFT", "RIGHT", "CHEST"]
for position in positions:
    run_observation_median_program(position)

save_results_to_file()
