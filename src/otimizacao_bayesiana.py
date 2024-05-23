import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import matthews_corrcoef, confusion_matrix
from keras.utils import to_categorical
from tensorflow import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Conv1D, Flatten, MaxPooling1D
import optuna
import csv

# Carregar dados
dados ='/home/dev/Área de trabalho/Combatente/Combatente/labels_and_data/data/right/conjunto_de_dados_magacc_dominio_tempo.npy'
rotulos ='/home/dev/Área de trabalho/Combatente/Combatente/labels_and_data/labels/right/rotulos_binario1_tempo.npy'

X = np.load(dados)
y = np.load(rotulos)

# Dividindo os dados em conjunto de treinamento e teste
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.3)

# Convertendo rótulos para categóricos
y_train = to_categorical(y_train)
y_val = to_categorical(y_val)

def objective(trial):
    # Definindo o espaço de busca dos hiperparâmetros
    filter_size = trial.suggest_int('filter_size', 8, 600, log=True)
    kernel_size = trial.suggest_int('kernel_size', 2, 6)
    num_layers = trial.suggest_int('num_layers', 2, 4)
    num_dense_layers = trial.suggest_int('num_dense_layers ', 1, 3)
    dense_neurons = trial.suggest_int('dense_neurons', 60, 320, log=True)
    dropout = trial.suggest_int('dropout', 2, 5, step=1) / 10.0
    learning_rate = trial.suggest_categorical('learning_rate', [0.0001, 0.0003, 0.0006, 0.001, 0.003, 0.006, 0.01])
    decision_threshold = trial.suggest_int('decision_threshold', 5, 9)/10.0

    max_pool = 2

    model = Sequential()

    for i in range(num_layers):
        if i == 0:
            model.add(Conv1D(filters=filter_size, kernel_size=kernel_size, activation="relu", input_shape=(480,1)))
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
    model.add(Dense(2, activation='softmax'))

    optimizer = keras.optimizers.Adam(learning_rate=learning_rate)
    model.compile(optimizer=optimizer, loss='categorical_crossentropy', metrics=['accuracy'])

    historico = model.fit(X_train, y_train, batch_size=32, epochs=25, validation_data=(X_val, y_val), verbose=1)

    y_pred_prob = model.predict(X_val)
    y_pred = (y_pred_prob[:, 1] >= decision_threshold).astype(int)

    mcc = matthews_corrcoef(y_val.argmax(axis=1), y_pred)

    # Imprimir os resultados na tela
    print(f"Trial {trial.number}: MCC = {mcc}, Params = {trial.params}")

    return mcc

# Criação do objeto de estudo
study = optuna.create_study(direction="maximize")

# Abertura do arquivo CSV em modo de escrita para o cabeçalho
with open("results.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile, delimiter=",")
    writer.writerow(["trial", "MCC", "hyperparameters"])  # cabeçalho

# Iteração dos trials e registro dos resultados
study.optimize(objective, n_trials=15)

# Obter o melhor trial
best_trial = study.best_trial
print("Best trial: MCC = {}".format(best_trial.value))

# Print dos melhores hiperparâmetros
print(study.best_params)
