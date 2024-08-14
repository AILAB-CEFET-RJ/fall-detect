import os
import numpy as np
from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import matthews_corrcoef, confusion_matrix, roc_auc_score, roc_curve, classification_report
import keras
from keras.utils import to_categorical
from keras.optimizers import SGD



from keras.models import Sequential
from keras.layers import Dense, Dropout, Conv1D, Flatten, MaxPooling1D
import optuna
import csv
import itertools
from sklearn.metrics import confusion_matrix

"Plot the training and validation accuracy graphs."
def plot_training_and_validation_accuracy_graphs(historic,output_dir,i,neural_network_type):

    acc = 'accuracy' if neural_network_type == "CNN1D" else "acc"
    val_acc = 'val_accuracy' if neural_network_type == "CNN1D" else 'val_acc'

    training_accuracy = historic.history[acc]
    validation_accuracy = historic.history[val_acc]

    epochs = range(1, len(training_accuracy) + 1)

    plt.plot(epochs, training_accuracy, "-g", label="Training Data Accuracy")
    plt.plot(epochs, validation_accuracy, "-b", label="Validation Data Accuracy")
    plt.legend()
    plt.xlabel('Epochs')
    plt.ylabel('Accuracy')
    plt.savefig(os.path.join(output_dir, f"accuracy_plot_model_{i}.png"))
    plt.close()

'''Use the predict function to predict the classes corresponding to each array of data representing an activity.'''
def return_ypredicted_and_ytrue(model,X_test,y_test,decision_threshold):
    y_predicted_probabilities = model.predict(X_test)
    y_predicted = (y_predicted_probabilities[:, 1] >= decision_threshold).astype(int)
    y_true = np.argmax(y_test, axis=1)

    return y_predicted,y_true,y_predicted_probabilities

'''Create the structure of the confusion matrix.'''
def create_confusion_matrix(y_true,y_predicted):
    cm = confusion_matrix(y_true, y_predicted)

    tn, fp, fn, tp = cm.ravel()

    return cm,tp, tn, fp, fn

'''Use the confusion matrix created by create_confusion_matrix and plot it as a graph.'''
def plot_confusion_matrix(cm,number_of_labels,output_dir,i):

    plt.imshow(cm, cmap=plt.cm.Blues)
    plt.title('Confusion Matrix')
    plt.colorbar()
    tick_marks = np.arange(0, number_of_labels)
    plt.xticks(tick_marks, rotation=90)
    plt.yticks(tick_marks)

    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], 'd'),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('Real Label')
    plt.xlabel('Predicted Label')
    plt.savefig(os.path.join(output_dir, f"confusion_matrix_model_{i}.png"))
    plt.close()

'''Create the the classification report as text file and save in the directory'''
def save_classification_report(y_predicted, y_true, number_of_labels, output_dir, i):
    target_names = np.arange(0, number_of_labels).astype(str)
    report = classification_report(y_true, y_predicted, target_names=target_names)
    with open(os.path.join(output_dir, f"classification_report_model_{i}.txt"), "w") as report_file:
        report_file.write(report)

'''Plot the ROC curve and save it in the output directory'''
def plot_roc_curve(y_predicted,y_true,output_dir, i):
    roc_auc = roc_auc_score(y_true, y_predicted)
    fpr, tpr, thresholds = roc_curve(y_true, y_predicted)
    plt.figure(figsize=(8, 6))
    plt.plot(fpr, tpr, color='blue', lw=2, label='Curva ROC (área = %0.2f)' % roc_auc)
    plt.plot([0, 1], [0, 1], color='gray', linestyle='--', lw=2)  # Diagonal
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('Taxa de Falso Positivo')
    plt.ylabel('Taxa de Verdadeiro Positivo')
    plt.title('ROC')
    plt.legend(loc="lower right")
    plt.grid(True)
    plt.savefig(os.path.join(output_dir, f"roc_curve_model_{i}.png"))
    plt.close()

'''Calculate the metrics that will be used to measure the model's effectiveness.'''
def calculate_metrics(tp, tn, fp, fn,y_test, y_predicted):

    mcc = matthews_corrcoef(y_test, y_predicted)
    sensitivity = tp / (tp + fn)
    specificity = tn / (tn + fp)
    precision = tp / (tp + fp)
    accuracy = (tp + tn) / (tp + tn + fp + fn)

    metrics = {
        "MCC": mcc,
        'Sensitivity': sensitivity,
        'Specificity': specificity,
        'Precision': precision,
        'Accuracy': accuracy
    }
    return metrics

'''Save the calculated metrics in a CSV file and store it in the output directory.'''
def record_the_metrics_in_the_table(metrics,tp, tn, fp, fn,i,output_dir):
    metrics["tp"] = tp
    metrics["tn"] = tn
    metrics["fp"] = fp
    metrics["fn"] = fn

    file_path = os.path.join(output_dir, f'metrics_model_{i}.csv')
    with open(file_path, "a", newline="") as csvfile:
        writer = csv.DictWriter(csvfile,
                                fieldnames=["Model", "MCC", "Sensitivity", "Specificity", "Precision", "Accuracy",
                                            "tp", "tn", "fp", "fn"])
        if csvfile.tell() == 0:  # Verifica se o arquivo está vazio para escrever o cabeçalho
            writer.writeheader()
        writer.writerow({"Model": i,
                         "MCC": metrics["MCC"],
                         "Sensitivity": metrics["Sensitivity"],
                         "Specificity": metrics["Specificity"],
                         "Precision": metrics["Precision"],
                         "Accuracy": metrics["Accuracy"],
                         "tp": metrics["tp"],
                         "tn": metrics["tn"],
                         "fp": metrics["fp"],
                         "fn": metrics["fn"]})

'''Save a text file with the best trial among the executed trials in the output directory.'''
def save_best_trial_to_csv(best_trial, best_params, file_path):
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Trial Number", best_trial.number])
        writer.writerow(["Value", best_trial.value])
        writer.writerow(["Parameters"])
        for key, value in best_params.items():
            writer.writerow([key, value])

'''Run all files related to metrics and graphs.'''
def save_results(model, historic, X_test, y_test,number_of_labels,i,decision_threshold,output_dir,neural_network_type):

    model.save(os.path.join(output_dir, f"model_{i}.keras"))
    plot_training_and_validation_accuracy_graphs(historic,output_dir,i,neural_network_type)
    y_predicted,y_true,y_predicted_probabilities = return_ypredicted_and_ytrue(model, X_test, y_test,decision_threshold)
    cm,tp, tn, fp, fn = create_confusion_matrix(y_true,y_predicted)
    plot_confusion_matrix(cm, number_of_labels,output_dir,i)
    save_classification_report(y_predicted, y_true, number_of_labels, output_dir, i)
    plot_roc_curve(y_predicted, y_true,output_dir,i)
    metrics = calculate_metrics(tp, tn, fp, fn, y_true, y_predicted)
    record_the_metrics_in_the_table(metrics,tp, tn, fp, fn,i,output_dir)

'''Create the structure of the CNN 1D network to be optimized.'''
def cnn1d_architecture(input_shape,X_train,y_train,X_val,y_val,filter_size,kernel_size,num_layers,num_dense_layers,dense_neurons,dropout,learning_rate,number_of_labels):
    max_pool = 2
    model = Sequential()
    for i in range(num_layers):
        if i == 0:
            model.add(Conv1D(filters=filter_size, kernel_size=kernel_size, activation="relu", input_shape= input_shape))
        else:
            if filter_size < kernel_size:
                filter_size = kernel_size
            filter_size *= 2
            model.add(Conv1D(filters=filter_size, kernel_size=kernel_size, activation="relu"))
        model.add(MaxPooling1D(pool_size=max_pool))
        model.add(Dropout(dropout))

    model.add(Flatten())
    for i in range(num_dense_layers):
        model.add(Dense(dense_neurons, activation='relu'))
    model.add(Dense(number_of_labels, activation='softmax'))

    optimizer = keras.optimizers.Adam(learning_rate=learning_rate)
    model.compile(optimizer=optimizer, loss='categorical_crossentropy', metrics=['accuracy'])

    historic = model.fit(X_train, y_train, batch_size=32, epochs=25, validation_data=(X_val, y_val), verbose=1)

    return model,historic

'''Create the structure of the MLP network to be optimized.'''
def mlp_architecture(input_dim,X_train,y_train,X_val,y_val,num_layers,dense_neurons,dropout,learning_rate,number_of_labels):
    model = Sequential()

    batch = int(len(y_train) / 30)

    for i in range(num_layers):
        if i == 0:
            model.add(Dense(dense_neurons, input_dim=input_dim, kernel_initializer='normal', activation='relu'))
            model.add(Dropout(dropout))
        else:
            model.add(Dense(dense_neurons, kernel_initializer='normal', activation='relu'))
            model.add(Dropout(dropout))

    model.add(Dense(number_of_labels, kernel_initializer='normal', activation='softmax'))

    optimizer = SGD(learning_rate=learning_rate)
    model.compile(loss="categorical_crossentropy", optimizer=optimizer, metrics=["acc"])
    historic = model.fit(X_train, y_train, epochs=300, batch_size=batch, validation_data=(X_val, y_val), verbose=1)

    return model, historic

'''Split the dataset into training, validation, and test sets.'''
def generate_training_testing_and_validation_sets(data=None, label=None):

        X = np.load(data)
        y = np.load(label)

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=42)
        X_test, X_val, y_test, y_val = train_test_split(X_test, y_test, test_size=0.5, random_state=42)

        y_train = to_categorical(y_train)
        y_test = to_categorical(y_test)
        y_val = to_categorical(y_val)

        return X_train, X_test, y_train, y_test, X_val, y_val

'''Define the search space and the parameters to be optimized.'''
def objective(trial,input_shape,X_train,y_train,X_val,y_val,neural_network_type,output_dir,number_of_labels):

    mcc = None

    if neural_network_type == "CNN1D":
        # Definindo o espaço de busca dos hiperparâmetros
        filter_size = trial.suggest_int('filter_size', 8, 600, log=True)
        kernel_size = trial.suggest_int('kernel_size', 2, 6)
        num_layers = trial.suggest_int('num_layers', 2, 4)
        num_dense_layers = trial.suggest_int('num_dense_layers', 1, 3)
        dense_neurons = trial.suggest_int('dense_neurons', 60, 320, log=True)
        dropout = trial.suggest_float('dropout', 0.1, 0.5, step=0.1)
        learning_rate = trial.suggest_categorical('learning_rate', [0.0001, 0.0003, 0.0006, 0.001, 0.003, 0.006, 0.01])
        decision_threshold = trial.suggest_float('decision_threshold', 0.5, 0.9,step=0.1)

        model,historic = cnn1d_architecture(input_shape,X_train,y_train,X_val,y_val,filter_size,kernel_size,
                                            num_layers,num_dense_layers,dense_neurons,dropout,learning_rate,number_of_labels)

        y_pred_prob = model.predict(X_val)
        y_pred = (y_pred_prob[:, 1] >= decision_threshold).astype(int)

        mcc = matthews_corrcoef(y_val.argmax(axis=1), y_pred)

        optimized_params = {
            "filter_size": filter_size,
            "kernel_size": kernel_size,
            "num_layers": num_layers,
            "num_dense_layers": num_dense_layers,
            "dense_neurons": dense_neurons,
            "dropout": dropout,
            "learning_rate": learning_rate,
            "decision_threshold": decision_threshold
        }

    elif neural_network_type == "MLP":

        num_layers = trial.suggest_int('num_layers', 1, 5)
        dense_neurons = trial.suggest_int('dense_neurons', 20, 4000, log=True)
        dropout = trial.suggest_float('dropout', 0.1, 0.5, step=0.1)
        learning_rate = trial.suggest_categorical('learning_rate', [0.001, 0.003, 0.005, 0.007, 0.01, 0.03, 0.05, 0.07])
        decision_threshold = trial.suggest_float('decision_threshold', 0.5, 0.9,step=0.1)

        model, historic = mlp_architecture(input_shape,X_train,y_train,X_val,y_val,num_layers,dense_neurons,dropout,learning_rate,number_of_labels)

        y_pred_prob = model.predict(X_val)
        y_pred = (y_pred_prob[:, 1] >= decision_threshold).astype(int)

        mcc = matthews_corrcoef(X_val.argmax(axis=1), y_pred)

        optimized_params = {
            "num_layers": num_layers,
            "dense_neurons": dense_neurons,
            "dropout": dropout,
            "learning_rate": learning_rate,
            "decision_threshold": decision_threshold
        }

    file_path = os.path.join(output_dir, 'optimization_results.csv')
    file_exists = os.path.isfile(file_path)

    with open(file_path, "a", newline='') as csvfile:
        fieldnames = ["Trial", "MCC"] + list(optimized_params.keys())
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()

        row = {"Trial": trial.number, "MCC": mcc}
        row.update(optimized_params)
        writer.writerow(row)

    return mcc

'''Creates an Optuna study object that defines the maximization direction to optimize the objective function.'''
def create_study_object(objective, input_shape, X_train, y_train, X_val, y_val, neural_network_type,neural_network_results_dir,number_of_labels):
    study = optuna.create_study(direction="maximize")

    study.optimize(lambda trial: objective(trial, input_shape, X_train, y_train, X_val, y_val, neural_network_type,neural_network_results_dir,number_of_labels), n_trials=20)

    best_trial = study.best_trial
    best_params = best_trial.params

    return best_trial,best_params

if __name__ == "__main__":
    pass

