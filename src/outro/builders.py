import pandas as pd
import os
import math
import numpy as np

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

    maggir = gyr_dataframe.loc[gyr_dataframe["sampling"] == i, "Magnitude"]
    maggir = maggir.reset_index(drop=True)
    maggir = maggir.drop(0)

    xgir = gyr_dataframe.loc[gyr_dataframe["sampling"] == i, "wx"]
    xgir = xgir.reset_index(drop=True)
    xgir = xgir.drop(0)

    ygir = gyr_dataframe.loc[gyr_dataframe["sampling"] == i, "wy"]
    ygir = ygir.reset_index(drop=True)
    ygir = ygir.drop(0)

    zgir = gyr_dataframe.loc[gyr_dataframe["sampling"] == i, "wz"]
    zgir = zgir.reset_index(drop=True)
    zgir = zgir.drop(0)

    return magacc,xacc,yacc,zacc,maggir,xgir,ygir,zgir

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
Returns the activity label for the four approaches
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
def generate_array_of_other_activities(data_array, array_size, data_array_list, fourier_transformed_data_array_list, multiple_class_label, three_class_label, binary_class_label_1, binary_class_label_2, add_labels_in_lista = None):
    parts = math.floor(len(data_array) / array_size)
    initial_index = 0
    final_index = array_size

    for i in range(parts):
        add_data_arrays_to_time_and_frequency_data_lists(initial_index,final_index, array_size, data_array,data_array_list,fourier_transformed_data_array_list)

        if add_labels_in_lista == "yes_acc":

            multiple_class_label_list_time_domain.append(multiple_class_label)
            three_class_label_list_time_domain.append(three_class_label)
            binary_class_label_1_list_time_domain.append(binary_class_label_1)
            binary_class_label_2_list_time_domain.append(binary_class_label_2)

        elif add_labels_in_lista == "yes_gir":

            multiple_class_label_list_frequency_domain.append(multiple_class_label)
            three_class_label_list_frequency_domain.append(three_class_label)
            binary_class_label_1_list_frequency_domain.append(binary_class_label_1)
            binary_class_label_2_list_frequency_domain.append(binary_class_label_2)

        initial_index += array_size
        final_index += array_size

def create_data_sets_for_training(position, activity, magacc, xacc, yacc, zacc, maggir, xgir, ygir, zgir):

    five_second_activity_list = ["FALL_1", "FALL_2","FALL_3","FALL_5","FALL_6","ADL_7","ADL_8","ADL_15"]
    transition_activities_list = ["OM_3", "OM_4", "OM_5","OM_6", "OM_7", "OM_8"]

    multiple_class_label,three_class_label,binary_class_label_1,binary_class_label_2 = create_labels(activity)

    array_size = 1050 if position == "CHEST" else 480

    if len(xgir) >= array_size and len(xacc) >= array_size:
        if activity in five_second_activity_list:

            generate_array_of_activities_lasting_5seconds(magacc, array_size, magacc_data_array_list,magacc_transformed_data_array_list)
            generate_array_of_activities_lasting_5seconds(xacc, array_size, xacc_data_array_list,xacc_transformed_data_array_list)
            generate_array_of_activities_lasting_5seconds(yacc, array_size, yacc_data_array_list,yacc_transformed_data_array_list)
            generate_array_of_activities_lasting_5seconds(zacc, array_size, zacc_data_array_list,zacc_transformed_data_array_list)
            generate_array_of_activities_lasting_5seconds(maggir, array_size, maggir_data_array_list,maggir_transformed_data_array_list)
            generate_array_of_activities_lasting_5seconds(xgir, array_size, xgir_data_array_list,xgir_transformed_data_array_list)
            generate_array_of_activities_lasting_5seconds(ygir, array_size, ygir_data_array_list,ygir_transformed_data_array_list)
            generate_array_of_activities_lasting_5seconds(zgir, array_size, zgir_data_array_list,zgir_transformed_data_array_list)

        elif activity in transition_activities_list:
            generate_array_of_transition_activities(magacc, array_size, magacc_data_array_list,magacc_transformed_data_array_list)
            generate_array_of_transition_activities(xacc, tamanho_do_array, xacc_data_array_list, xacc_data_array_list_transformada)
            generate_array_of_transition_activities(yacc, tamanho_do_array, yacc_data_array_list, yacc_data_array_list_transformada)
            generate_array_of_transition_activities(zacc, tamanho_do_array, lista_array_de_dados_zacc, lista_array_de_dados_zacc_transformada)
            generate_array_of_transition_activities(maggir, tamanho_do_array, lista_array_de_dados_maggir, lista_array_de_dados_maggir_transformada)
            generate_array_of_transition_activities(xgir, tamanho_do_array, lista_array_de_dados_xgir, lista_array_de_dados_xgir_transformada)
            generate_array_of_transition_activities(ygir, tamanho_do_array, lista_array_de_dados_ygir, lista_array_de_dados_ygir_transformada)
            generate_array_of_transition_activities(zgir, tamanho_do_array, lista_array_de_dados_zgir, lista_array_de_dados_zgir_transformada)

            multiple_class_label_list_time_domain.append( multiple_class_label)
            three_class_label_list_time_domain.append(rotulo_tres)
            binary_class_label_1_list_time_domain.append(rotulo_binario1)
            binary_class_label_2_list_time_domain.append(rotulo_binario2)
            multiple_class_label_list_frequency_domain.append( multiple_class_label)
            three_class_label_list_frequency_domain.append(rotulo_tres)
            binary_class_label_1_list_frequency_domain.append(rotulo_binario1)
            binary_class_label_2_list_frequency_domain.append(rotulo_binario2)
        else:
            generate_array_of_other_activities(magacc, tamanho_do_array,  magacc_data_array_list,  multiple_class_label, rotulo_tres, rotulo_binario1, rotulo_binario2,  magacc_data_array_list_transformada, "sim_acc")
            generate_array_of_other_activities(xacc, tamanho_do_array, xacc_data_array_list,  multiple_class_label, rotulo_tres, rotulo_binario1, rotulo_binario2, xacc_data_array_list_transformada)
            generate_array_of_other_activities(yacc, tamanho_do_array, yacc_data_array_list,  multiple_class_label, rotulo_tres, rotulo_binario1, rotulo_binario2, yacc_data_array_list_transformada)
            generate_array_of_other_activities(zacc, tamanho_do_array, lista_array_de_dados_zacc,  multiple_class_label, rotulo_tres, rotulo_binario1, rotulo_binario2, lista_array_de_dados_zacc_transformada)
            generate_array_of_other_activities(maggir, tamanho_do_array, lista_array_de_dados_maggir,  multiple_class_label, rotulo_tres, rotulo_binario1, rotulo_binario2, lista_array_de_dados_maggir_transformada, "sim_gir")
            generate_array_of_other_activities(xgir, tamanho_do_array, lista_array_de_dados_xgir,  multiple_class_label, rotulo_tres, rotulo_binario1, rotulo_binario2, lista_array_de_dados_xgir_transformada)
            generate_array_of_other_activities(ygir, tamanho_do_array, lista_array_de_dados_ygir,  multiple_class_label, rotulo_tres, rotulo_binario1, rotulo_binario2, lista_array_de_dados_ygir_transformada)
            generate_array_of_other_activities(zgir, tamanho_do_array, lista_array_de_dados_zgir,  multiple_class_label, rotulo_tres, rotulo_binario1, rotulo_binario2, lista_array_de_dados_zgir_transformada)


def plotar_activitys(df_acc,df_gir,df_sampling,diretorio1,diretorio2,diretorio3,diretorio4,diretorio5, diretorio6, diretorio7,
                                     diretorio8,arquivo_erros):
    lista_de_nomes = []

    for i in (df_sampling["id"]):


        activity = (df_sampling.loc[df_sampling["id"] == i, "exercise"].iloc[0])

        magacc,xacc,yacc,zacc,tempo_segundos_acc,maggir,xgir,ygir,zgir,tempo_segundos_gir = section_data_array(df_acc, df_gir, i)

        criar_conjuntos_de_dados_para_treino(position, activity, magacc, xacc, yacc, zacc, maggir, xgir, ygir, zgir)

        #plotar_grafico_das_activity(i, lista_de_nomes,df_sampling, magacc, xacc, yacc, zacc, tempo_segundos_acc, maggir, xgir,ygir, zgir,
                                     #tempo_segundos_gir,diretorio1, diretorio2, diretorio3, diretorio4, diretorio5, diretorio6, diretorio7,
                                     #diretorio8, arquivo_erros)



diretorio_principal= "/home/dev/Área de trabalho/Combatente/Combatente/Database"

lista_de_subdiretorios = os.listdir(diretorio_principal)

lista_de_subdiretorios.sort(key=sort_by_number)

position = "RIGHT"

if position == "CHEST":
    #diretorios acc
    diretorio1 ="/home/dev/Área de trabalho/Combatente/Combatente/imagens_new_database/Chest/acelerometro/mag"
    diretorio2 ="/home/dev/Área de trabalho/Combatente/Combatente/imagens_new_database/Chest/acelerometro/x"
    diretorio3 ="/home/dev/Área de trabalho/Combatente/Combatente/imagens_new_database/Chest/acelerometro/y"
    diretorio4 ="/home/dev/Área de trabalho/Combatente/Combatente/imagens_new_database/Chest/acelerometro/z"
    #diretorios gir
    diretorio5 ="/home/dev/Área de trabalho/Combatente/Combatente/imagens_new_database/Chest/giroscopio/mag"
    diretorio6 ="/home/dev/Área de trabalho/Combatente/Combatente/imagens_new_database/Chest/giroscopio/x"
    diretorio7 ="/home/dev/Área de trabalho/Combatente/Combatente/imagens_new_database/Chest/giroscopioy"
    diretorio8 ="/home/dev/Área de trabalho/Combatente/Combatente/imagens_new_database/Chest/giroscopio/z"

    diretorio_rotulos = "/home/dev/Área de trabalho/Combatente/Combatente/labels_and_data/labels/chest"
    diretorio_array_dados = "/home/dev/Área de trabalho/Combatente/Combatente/labels_and_data/data/chest"

elif position == "LEFT":
    # diretorios acc
    diretorio1 = "/home/dev/Área de trabalho/Combatente/Combatente/imagens_new_database/Left/acelerometro/mag"
    diretorio2 = "/home/dev/Área de trabalho/Combatente/Combatente/imagens_new_database/Left/acelerometro/x"
    diretorio3 = "/home/dev/Área de trabalho/Combatente/Combatente/imagens_new_database/Left/acelerometro/y"
    diretorio4 = "/home/dev/Área de trabalho/Combatente/Combatente/imagens_new_database/Left/acelerometro/z"
    # diretorios gir
    diretorio5 = "/home/dev/Área de trabalho/Combatente/Combatente/imagens_new_database/Left/giroscopio/mag"
    diretorio6 = "/home/dev/Área de trabalho/Combatente/Combatente/imagens_new_database/Left/giroscopio/x"
    diretorio7 = "/home/dev/Área de trabalho/Combatente/Combatente/imagens_new_database/Left/giroscopioy"
    diretorio8 = "/home/dev/Área de trabalho/Combatente/Combatente/imagens_new_database/Left/giroscopio/z"

    diretorio_rotulos = "/home/dev/Área de trabalho/Combatente/Combatente/labels_and_data/labels/left"
    diretorio_array_dados = "/home/dev/Área de trabalho/Combatente/Combatente/labels_and_data/data/left"
else:
    # diretorios acc
    diretorio1 = "/home/dev/Área de trabalho/Combatente/Combatente/imagens_new_database/Right/acelerometro/mag"
    diretorio2 = "/home/dev/Área de trabalho/Combatente/Combatente/imagens_new_database/Right/acelerometro/x"
    diretorio3 = "/home/dev/Área de trabalho/Combatente/Combatente/imagens_new_database/Right/acelerometro/y"
    diretorio4 = "/home/dev/Área de trabalho/Combatente/Combatente/imagens_new_database/Right/acelerometro/z"
    # diretorios gir
    diretorio5 = "/home/dev/Área de trabalho/Combatente/Combatente/imagens_new_database/Right/giroscopio/mag"
    diretorio6 = "/home/dev/Área de trabalho/Combatente/Combatente/imagens_new_database/Right/giroscopio/x"
    diretorio7 = "/home/dev/Área de trabalho/Combatente/Combatente/imagens_new_database/Right/giroscopio/y"
    diretorio8 = "/home/dev/Área de trabalho/Combatente/Combatente/imagens_new_database/Right/giroscopio/z"

    diretorio_rotulos = "/home/dev/Área de trabalho/Combatente/Combatente/labels_and_data/labels/right"
    diretorio_array_dados = "/home/dev/Área de trabalho/Combatente/Combatente/labels_and_data/data/right"

arquivo_erros = "/home/dev/Área de trabalho/Combatente/Combatente/imagens_new_database/erros"

#magacc
magacc_data_array_list = []
#xacc
xacc_data_array_list = []
#yacc
yacc_data_array_list = []
#zacc
zacc_data_array_list = []

#maggir
maggir_data_array_list = []
#xgir
xgir_data_array_list = []
#ygir
ygir_data_array_list = []
#zgir
zgir_data_array_list = []

#magacc in the frequency domain
magacc_transformed_data_array_list = []
#xacc in the frequency domain
xacc_transformed_data_array_list = []
#yacc in the frequency domain
yacc_transformed_data_array_list = []
#zacc in the frequency domain
zacc_transformed_data_array_list = []

#maggir in the frequency domain
maggir_transformed_data_array_list = []
#xgir in the frequency domain
xgir_transformed_data_array_list = []
#ygir in the frequency domain
ygir__transformed_data_array_list= []
#zgir in the frequency domain
zgir__transformed_data_array_list = []

multiple_class_label_list_time_domain = []
three_class_label_list_time_domain = []
binary_class_label_1_list_time_domain = []
binary_class_label_2_list_time_domain = []

multiple_class_label_list_frequency_domain = []
three_class_label_list_frequency_domain = []
binary_class_label_1_list_frequency_domain = []
binary_class_label_2_list_frequency_domain = []


for subdiretorio in lista_de_subdiretorios:
    acc,gir,sampling = get_file_path(diretorio_principal, subdiretorio, position)
    df_acc,df_gir,df_sampling = create_dataframe(acc, gir, sampling)
    plotar_activitys(df_acc, df_gir, df_sampling,diretorio1,diretorio2,diretorio3,diretorio4,diretorio5, diretorio6, diretorio7,
                                     diretorio8,arquivo_erros)


conjunto_rotulos_multiplos_tempo = np.asarray(multiple_class_label_list_time_domain)
conjunto_rotulos_tres_labels_tempo = np.asarray(three_class_label_list_time_domain)
conjunto_rotulos_binario1_tempo = np.asarray(binary_class_label_1_list_time_domain)
conjunto_rotulos_binario2_tempo= np.asarray(binary_class_label_2_list_time_domain)

conjunto_rotulos_multiplos_freq = np.asarray(multiple_class_label_list_frequency_domain)
conjunto_rotulos_tres_labels_freq = np.asarray(three_class_label_list_frequency_domain)
conjunto_rotulos_binario1_freq = np.asarray(binary_class_label_1_list_frequency_domain)
conjunto_rotulos_binario2_freq = np.asarray(binary_class_label_2_list_frequency_domain)

np.save(os.path.join(diretorio_rotulos, 'rotulos_multiplos_tempo.npy'), conjunto_rotulos_multiplos_tempo)
np.save(os.path.join(diretorio_rotulos, 'rotulos_tres_labels_tempo.npy'), conjunto_rotulos_tres_labels_tempo)
np.save(os.path.join(diretorio_rotulos, 'rotulos_binario1_tempo.npy'), conjunto_rotulos_binario1_tempo)
np.save(os.path.join(diretorio_rotulos, 'rotulos_binario2_tempo.npy'), conjunto_rotulos_binario2_tempo)

np.save(os.path.join(diretorio_rotulos, 'rotulos_multiplos_freq.npy'), conjunto_rotulos_multiplos_freq)
np.save(os.path.join(diretorio_rotulos, 'rotulos_tres_labels_freq.npy'), conjunto_rotulos_tres_labels_freq)
np.save(os.path.join(diretorio_rotulos, 'rotulos_binario1_freq.npy'), conjunto_rotulos_binario1_freq)
np.save(os.path.join(diretorio_rotulos, 'rotulos_binario2_freq.npy'), conjunto_rotulos_binario2_freq)

conjunto_de_dados_magacc= np.asarray( magacc_data_array_list)
conjunto_de_dados_magacc_transformada = np.asarray( magacc_data_array_list_transformada)
conjunto_de_dados_xacc= np.asarray(xacc_data_array_list)
conjunto_de_dados_xacc_transformada = np.asarray(xacc_data_array_list_transformada)
conjunto_de_dados_yacc= np.asarray(yacc_data_array_list)
conjunto_de_dados_yacc_transformada = np.asarray(yacc_data_array_list_transformada)
conjunto_de_dados_zacc= np.asarray(lista_array_de_dados_zacc)
conjunto_de_dados_zacc_transformada = np.asarray(lista_array_de_dados_zacc_transformada)

conjunto_de_dados_maggir= np.asarray(lista_array_de_dados_maggir)
conjunto_de_dados_maggir_transformada = np.asarray(lista_array_de_dados_maggir_transformada)
conjunto_de_dados_xgir= np.asarray(lista_array_de_dados_xgir)
conjunto_de_dados_xgir_transformada = np.asarray(lista_array_de_dados_xgir_transformada)
conjunto_de_dados_ygir= np.asarray(lista_array_de_dados_ygir)
conjunto_de_dados_ygir_transformada = np.asarray(lista_array_de_dados_ygir_transformada)
conjunto_de_dados_zgir= np.asarray(lista_array_de_dados_zgir)
conjunto_de_dados_zgir_transformada = np.asarray(lista_array_de_dados_zgir_transformada)

np.save(os.path.join(diretorio_array_dados, 'conjunto_de_dados_magacc_dominio_tempo.npy'), conjunto_de_dados_magacc)
np.save(os.path.join(diretorio_array_dados, 'conjunto_de_dados_magacc_dominio_frequencia.npy'), conjunto_de_dados_magacc_transformada)
np.save(os.path.join(diretorio_array_dados, 'conjunto_de_dados_xacc_dominio_tempo.npy'), conjunto_de_dados_xacc)
np.save(os.path.join(diretorio_array_dados, 'conjunto_de_dados_xacc_dominio_frequencia.npy'), conjunto_de_dados_xacc_transformada)
np.save(os.path.join(diretorio_array_dados, 'conjunto_de_dados_yacc_dominio_tempo.npy'), conjunto_de_dados_yacc)
np.save(os.path.join(diretorio_array_dados, 'conjunto_de_dados_yacc_dominio_frequencia.npy'), conjunto_de_dados_yacc_transformada)
np.save(os.path.join(diretorio_array_dados, 'conjunto_de_dados_zacc_dominio_tempo.npy'), conjunto_de_dados_zacc)
np.save(os.path.join(diretorio_array_dados, 'conjunto_de_dados_zacc_dominio_frequencia.npy'), conjunto_de_dados_zacc_transformada)

np.save(os.path.join(diretorio_array_dados, 'conjunto_de_dados_maggir_dominio_tempo.npy'), conjunto_de_dados_maggir)
np.save(os.path.join(diretorio_array_dados, 'conjunto_de_dados_maggir_dominio_frequencia.npy'), conjunto_de_dados_maggir_transformada)
np.save(os.path.join(diretorio_array_dados, 'conjunto_de_dados_xgir_dominio_tempo.npy'), conjunto_de_dados_xgir)
np.save(os.path.join(diretorio_array_dados, 'conjunto_de_dados_xgir_dominio_frequencia.npy'), conjunto_de_dados_xgir_transformada)
np.save(os.path.join(diretorio_array_dados, 'conjunto_de_dados_ygir_dominio_tempo.npy'), conjunto_de_dados_ygir)
np.save(os.path.join(diretorio_array_dados, 'conjunto_de_dados_ygir_dominio_frequencia.npy'), conjunto_de_dados_ygir_transformada)
np.save(os.path.join(diretorio_array_dados, 'conjunto_de_dados_zgir_dominio_tempo.npy'), conjunto_de_dados_zgir)
np.save(os.path.join(diretorio_array_dados, 'conjunto_de_dados_zgir_dominio_frequencia.npy'), conjunto_de_dados_zgir_transformada)



