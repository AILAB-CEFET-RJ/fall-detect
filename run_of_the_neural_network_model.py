import csv
import os
from builders.model_builders import generate_training_testing_and_validation_sets, create_study_object, objective, \
    cnn1d_architecture, save_results, mlp_architecture, save_best_trial_to_csv

''' EXECUTION OF THE BAYESIAN OPTIMIZATION PROGRAM AND SUBSEQUENT MODEL TRAINING '''

position = "left"
#position = "chest"
#position = "right"

domain = "time"
#domain = "frequency"

#label_type = "multiple_one"
label_type = "multiple_two"
#label_type = "binary_one"
#label_type = "binary_two"

number_of_labels = 37 if label_type == "multiple_one" else 26 if label_type == "multiple_two" else 2

current_directory = os.path.dirname(__file__)

data_path = os.path.join(current_directory,"labels_and_data","data","chest") if position == "chest" \
            else os.path.join(current_directory,"labels_and_data","data","left") if position == "left" \
            else os.path.join(current_directory,"labels_and_data","data","right")
label_path = os.path.join(current_directory,"labels_and_data","labels","chest") if position == "chest" \
            else os.path.join(current_directory,"labels_and_data","labels","left") if position == "left" \
            else os.path.join(current_directory,"labels_and_data","labels","right")

if domain == "frequency":
    array_size = 510 if position == "chest" else 225
else:
    array_size = 1020 if position == "chest" else 450

neural_network_scenarios = {
    "Sc1_acc_T": [os.path.join(data_path,'magacc_time_domain_data_array.npy'), (array_size,1)], # for Sc1_CNN1D_acc_T and Sc1_MLP_acc_T
    "Sc1_gyr_T": [os.path.join(data_path,'maggyr_time_domain_data_array.npy'), (array_size,1)], # for Sc1_CNN1D_gyr_T and Sc1_MLP_gyr_T
    "Sc1_acc_F": [os.path.join(data_path,'magacc_frequency_domain_data_array.npy'), (array_size,1)], # for Sc1_CNN1D_acc_F and Sc1_MLP_acc_F
    "Sc1_gyr_F": [os.path.join(data_path,'maggyr_frequency_domain_data_array.npy'), (array_size,1)],  # for Sc1_CNN1D_gyr_F and Sc1_MLP_gyr_F
    "Sc_2_acc_T": [os.path.join(data_path,'acc_x_y_z_axes_time_domain_data_array.npy'), (array_size,3)], # for Sc_2_CNN1D_acc_T and Sc_2_MLP_acc_T
    "Sc_2_gyr_T": [os.path.join(data_path,'gyr_x_y_z_axes_time_domain_data_array.npy'), (array_size,3)], # for Sc_2_CNN1D_gyr_T and Sc_2_MLP_gyr_T
    "Sc_2_acc_F": [os.path.join(data_path,'acc_x_y_z_axes_frequency_domain_data_array.npy'), (array_size,3)], # for Sc_2_CNN1D_acc_F and Sc_2_MLP_acc_F
    "Sc_2_gyr_F": [os.path.join(data_path,'gyr_x_y_z_axes_frequency_domain_data_array.npy'), (array_size,3)], # for Sc_2_CNN1D_gyr_F and Sc_2_MLP_gyr_F
    "Sc_3_T": [os.path.join(data_path,'magacc_and_maggyr_time_domain_data_array.npy'), (array_size,2)], # for Sc_3_CNN1D_T and Sc_3_MLP_T
    "Sc_3_F": [os.path.join(data_path,'magacc_and_maggyr_frequency_domain_data_array.npy'), (array_size,2)], # for Sc_3_CNN1D_F and Sc_3_MLP_F
    "Sc_4_T": [os.path.join(data_path,'acc_and_gyr_three_axes_time_domain_data_array.npy'), (array_size,6)], # for Sc_4_CNN1D_T and Sc_4_MLP_T
    "Sc_4_F": [os.path.join(data_path,'acc_and_gyr_three_axes_frequency_domain_data_array.npy'), (array_size,6)], # for Sc_4_CNN1D_F and Sc_4_MLP_F
}

scenario = "Sc1_acc_T"  #Change the scenario here according to the network you want to train

data = neural_network_scenarios[scenario]

neural_network_type = "CNN1D" #Comment or uncomment to train or not train the cnn1d network.
#neural_network_type = "MLP" #Comment or uncomment to train or not train the MLP network.

label_index = 1 if label_type == "multiple_one" else 2 if label_type == "multiple_two" else 3 if label_type == "binary_one" else 4
label_options = {1:"multiple_class_label_1.npy",2:"multiple_class_label_2.npy",3:"binary_class_label_1.npy",4:"binary_class_label_2.npy"}

labels = os.path.join(label_path, label_options.get(label_index))

X_train, X_test, y_train, y_test, X_val, y_val = generate_training_testing_and_validation_sets(data[0],labels)
input_shape = data[1] if neural_network_type == "CNN1D" else array_size

output_dir = os.path.join(current_directory,"output")
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

if neural_network_type == "CNN1D":

    neural_network_results_dir = os.path.join(output_dir, "cnn1d")
    scenario_dir = os.path.join(os.path.join(neural_network_results_dir, scenario,label_type))

    if not os.path.exists(neural_network_results_dir):
        os.makedirs(neural_network_results_dir)
    if not os.path.exists(scenario_dir):
        os.makedirs(scenario_dir)
else:

    neural_network_results_dir = os.path.join(output_dir, "mlp")
    scenario_dir = os.path.join(os.path.join(neural_network_results_dir, scenario,label_type))

    if not os.path.exists(neural_network_results_dir):
        os.makedirs(neural_network_results_dir)
    if not os.path.exists(scenario_dir):
        os.makedirs(scenario_dir)

print("\n")
print("Starting Optimization")
print("\n")

best_trial,best_params = create_study_object(objective, input_shape, X_train, y_train, X_val, y_val, neural_network_type,neural_network_results_dir,number_of_labels)

csv_file_path = os.path.join(scenario_dir, 'best_trial.csv')
save_best_trial_to_csv(best_trial, best_params, csv_file_path)

print("\n")
print("Starting Training")
print("\n")

for i in range(1, 4):
    if neural_network_type == "CNN1D":

        mlp_output_dir = os.path.join(scenario_dir, f'CNN1D_model_{i}')
        if not os.path.exists(mlp_output_dir):
            os.makedirs(mlp_output_dir)

        model,historic = cnn1d_architecture(
                input_shape,
                X_train,
                y_train,
                X_val,
                y_val,
                best_params['filter_size'],
                best_params['kernel_size'],
                best_params['num_layers'],
                best_params['num_dense_layers'],
                best_params['dense_neurons'],
                best_params['dropout'],
                best_params['learning_rate'],
                number_of_labels)
        decision_threshold = best_params['decision_threshold']
        save_results(model, historic, X_test, y_test, number_of_labels, i, decision_threshold, mlp_output_dir,neural_network_type)

    elif neural_network_type == "MLP":

        mlp_output_dir = os.path.join(scenario_dir, f'MLP_model_{i}')
        if not os.path.exists(mlp_output_dir):
            os.makedirs(mlp_output_dir)

        model, historic = mlp_architecture(
            input_shape,
            X_train,
            y_train,
            X_val,
            y_val,
            best_params['num_layers'],
            best_params['dense_neurons'],
            best_params['dropout'],
            best_params['learning_rate'],
            number_of_labels)
        decision_threshold = best_params['decision_threshold']
        save_results(model, historic, X_test, y_test, number_of_labels, i, decision_threshold,mlp_output_dir,neural_network_type)
