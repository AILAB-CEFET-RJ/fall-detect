import pandas as pd
import os
import math
import matplotlib.pyplot as plt
import numpy as np



def ordenar_por_numero(id):
    return int(id[2:])

def adicionar_coluna_de_magnitude(dataframe,sensor = None):
    letra_inicial = None

    if sensor == "acc":
        letra_inicial = "a"
    else:
        letra_inicial = "w"

    forca_resultante = []
    i = 0

    while i < len(dataframe[f'{letra_inicial}x']):
        resultante = math.sqrt((dataframe[f'{letra_inicial}x'][i]) ** 2 + (dataframe[f'{letra_inicial}y'][i]) ** 2 + (dataframe[f'{letra_inicial}z'][i]) ** 2)
        forca_resultante.append(resultante)
        i += 1
    dataframe.insert(5, "Magnitude", forca_resultante, True)

def gerar_serie_de_tempo(timestamp):
    timestamp = timestamp.reset_index(drop=True)
    timestamp = timestamp.drop(0)
    timestamp = timestamp.reset_index(drop=True)

    tempo_segundos = [0.000]
    k = 0
    while k < len(timestamp):
        if k!= len(timestamp) - 1:
            variacao_tempo = (timestamp[k + 1]) - (timestamp[0])
            temp_seg = variacao_tempo / 1000
            tempo_segundos.append(temp_seg)

        k += 1
    return tempo_segundos

def plot_grafico(array,tempo,nome_figura,diretorio,arquivo_erros):
    try:
        plt.ylim(-80, 150)
        plt.plot(tempo,array,label="Magnitude")
        plt.legend()
        plt.xlabel("Time")
        plt.savefig(os.path.join(diretorio,nome_figura))
        plt.close()
    except Exception as e:
        mensagem_erro = f"Erro ao plotar o gráfico {nome_figura}: {str(e)}"
        print(mensagem_erro)

        # Registrar o erro em um arquivo
        with open(arquivo_erros, "a") as arquivo:
            arquivo.write(mensagem_erro + "\n")

def obter_caminhos_dos_arquivos(diretorio_principal, subdiretorio, posicao):
    caminho_do_subdiretorio = os.path.join(diretorio_principal, subdiretorio)
    caminho_do_subdiretorio_do_subdiretorio = os.path.join(caminho_do_subdiretorio, posicao)

    nome_do_arquivo = f'{subdiretorio}_{posicao}_acceleration.csv'
    nome_do_arquivo_2 = f'{subdiretorio}_{posicao}_sampling.csv'
    nome_do_arquivo_3 = f'{subdiretorio}_{posicao}_angular_speed.csv'

    arquivo_sampling = os.path.join(caminho_do_subdiretorio_do_subdiretorio, nome_do_arquivo_2)
    arquivo_acc = os.path.join(caminho_do_subdiretorio_do_subdiretorio, nome_do_arquivo)
    arquivo_gir = os.path.join(caminho_do_subdiretorio_do_subdiretorio, nome_do_arquivo_3)

    return arquivo_acc,arquivo_gir,arquivo_sampling

def gerar_dataframe(arquivo_acc,arquivo_gir,arquivo_sampling):

    acc = pd.DataFrame(pd.read_csv(arquivo_acc))
    gir = pd.DataFrame(pd.read_csv(arquivo_gir))
    sampling = pd.DataFrame(pd.read_csv(arquivo_sampling))

    adicionar_coluna_de_magnitude(acc,"acc")
    adicionar_coluna_de_magnitude(gir)

    return acc,gir,sampling

def transformada(serie_temporal):
    serie_temp_alterada = []
    media_serie_temp = np.mean(serie_temporal)

    for i in serie_temporal:
        dado = i - media_serie_temp
        serie_temp_alterada.append(dado)
    serie_temp_alt = np.array(serie_temp_alterada)

    return np.abs(np.fft.fft(serie_temp_alt))

def gerar_rotulos(atividade):
    labels_multiplos = {"ADL_1": 0, "ADL_2": 1, "ADL_3": 2, "ADL_4": 3, "ADL_5": 4, "ADL_6": 5, "ADL_7": 6, "ADL_8": 7,
                        "ADL_11": 8, "ADL_12": 9, "ADL_13": 10, "ADL_14": 11, "ADL_15": 12, "OM_1": 13, "OM_2": 14,
                        "OM_3": 15, "OM_4": 16, "OM_5": 17, "OM_6": 18, "OM_7": 19, "OM_8": 20, "OM_9": 21,
                        "FALL_1": 22, "FALL_2": 23, "FALL_3": 24, "FALL_5": 25, "FALL_6": 25}

    labels_tres = {"ADL_1": 1, "ADL_2": 1, "ADL_3": 1, "ADL_4": 1, "ADL_5": 1, "ADL_6": 1, "ADL_7": 1, "ADL_8": 1,
                   "ADL_11": 1, "ADL_12": 1, "ADL_13": 1, "ADL_14": 1, "ADL_15": 1, "OM_1": 2,
                   "OM_2": 2, "OM_3": 2, "OM_4": 2, "OM_5": 2, "OM_6": 2, "OM_7": 2, "OM_8": 2, "OM_9": 2,
                   "FALL_1": 0, "FALL_2": 0, "FALL_3": 0, "FALL_5": 0, "FALL_6": 0}

    '''Labels binario 1 as atividades 0M6 a OM8 são consideradas como quedas'''
    labels_binario1 = {"ADL_1": 1, "ADL_2": 1, "ADL_3": 1, "ADL_4": 1, "ADL_5": 1, "ADL_6": 1, "ADL_7": 1, "ADL_8": 1,
                       "ADL_11": 1, "ADL_12": 1, "ADL_13": 1, "ADL_14": 1, "ADL_15": 1, "OM_1": 1,
                       "OM_2": 1, "OM_3": 1, "OM_4": 1, "OM_5": 1, "OM_6": 0, "OM_7": 0, "OM_8": 0, "OM_9": 1,
                       "FALL_1": 0, "FALL_2": 0, "FALL_3": 0, "FALL_5": 0, "FALL_6": 0}

    '''Labels binario 2 as atividades 0M6 a OM8 são consideradas como não quedas'''
    labels_binario2 = {"ADL_1": 1, "ADL_2": 1, "ADL_3": 1, "ADL_4": 1, "ADL_5": 1, "ADL_6": 1, "ADL_7": 1, "ADL_8": 1,
                       "ADL_11": 1, "ADL_12": 1, "ADL_13": 1, "ADL_14": 1, "ADL_15": 1, "OM_1": 1,
                       "OM_2": 1, "OM_3": 1, "OM_4": 1, "OM_5": 1, "OM_6": 0, "OM_7": 0, "OM_8": 0, "OM_9": 1,
                       "FALL_1": 0, "FALL_2": 0, "FALL_3": 0, "FALL_5": 0, "FALL_6": 0}

    rotulo_multiplos = labels_multiplos.get(atividade)
    rotulo_tres = labels_tres.get(atividade)
    rotulo_binario1 = labels_binario1.get(atividade)
    rotulo_binario2 = labels_binario2.get(atividade)

    return rotulo_multiplos,rotulo_tres,rotulo_binario1,rotulo_binario2

def gerar_array_de_atividades_de_5s(valor_maximo,atividade,serie_de_dados,tamanho_do_array,lista_array_de_dados,lista_array_de_dados_transformada,rotulo_multiplos ,rotulo_tres,rotulo_binario1,rotulo_binario2,imprimir = None):

    if atividade[0:4] == "FALL":
        if imprimir == "sim":
            print(valor_maximo)
            if valor_maximo > 35:
                array_de_dados = serie_de_dados[:tamanho_do_array]
                nparray_de_dados = np.array(array_de_dados)
                nparray_de_dados = np.expand_dims(nparray_de_dados, axis=1)
                lista_array_de_dados.append(nparray_de_dados)

                array_de_dados_transformada = transformada(array_de_dados)
                array_de_dados_transformada = array_de_dados_transformada [:int(tamanho_do_array/2)]
                nparray_de_dados_transformada = np.array(array_de_dados_transformada)
                nparray_de_dados_transformada = np.expand_dims(nparray_de_dados_transformada, axis=1)
                lista_array_de_dados_transformada.append(nparray_de_dados_transformada)

                lista_de_rotulos_multiplo_tempo.append(rotulo_multiplos)
                lista_de_rotulos_tres_labels_tempo.append(rotulo_tres)
                lista_de_rotulos_binario1_tempo.append(rotulo_binario1)
                lista_de_rotulos_binario2_tempo.append(rotulo_binario2)
                lista_de_rotulos_multiplo_freq.append(rotulo_multiplos)
                lista_de_rotulos_tres_labels_freq.append(rotulo_tres)
                lista_de_rotulos_binario1_freq.append(rotulo_binario1)
                lista_de_rotulos_binario2_freq.append(rotulo_binario2)
    else:
        array_de_dados = serie_de_dados[:tamanho_do_array]
        nparray_de_dados = np.array(array_de_dados)
        nparray_de_dados = np.expand_dims(nparray_de_dados, axis=1)
        lista_array_de_dados.append(nparray_de_dados)

        array_de_dados_transformada = transformada(array_de_dados)
        array_de_dados_transformada = array_de_dados_transformada[:int(tamanho_do_array / 2)]
        nparray_de_dados_transformada = np.array(array_de_dados_transformada)
        nparray_de_dados_transformada = np.expand_dims(nparray_de_dados_transformada, axis=1)
        lista_array_de_dados_transformada.append(nparray_de_dados_transformada)

        lista_de_rotulos_multiplo_tempo.append(rotulo_multiplos)
        lista_de_rotulos_tres_labels_tempo.append(rotulo_tres)
        lista_de_rotulos_binario1_tempo.append(rotulo_binario1)
        lista_de_rotulos_binario2_tempo.append(rotulo_binario2)
        lista_de_rotulos_multiplo_freq.append(rotulo_multiplos)
        lista_de_rotulos_tres_labels_freq.append(rotulo_tres)
        lista_de_rotulos_binario1_freq.append(rotulo_binario1)
        lista_de_rotulos_binario2_freq.append(rotulo_binario2)

def gerar_array_de_atividades_de_transicao(serie_de_dados,tamanho_do_array,lista_array_de_dados,lista_array_de_dados_transformada):
    valor_maximo = max(serie_de_dados)
    indice_do_valor_maximo = int(serie_de_dados.loc[serie_de_dados == valor_maximo].index[0])
    indice_inicial = int(indice_do_valor_maximo - (tamanho_do_array / 2))
    indice_final = int(indice_do_valor_maximo + (tamanho_do_array / 2))

    if indice_inicial < 0:
        indice_inicial = 0
        indice_final = tamanho_do_array
    elif indice_final > int(serie_de_dados.index[-1]):
        indice_final = int(serie_de_dados.index[-1])
        indice_inicial = indice_final - tamanho_do_array

    array_de_dados = serie_de_dados[indice_inicial:indice_final]
    nparray_de_dados = np.array(array_de_dados)
    nparray_de_dados = np.expand_dims(nparray_de_dados, axis=1)
    lista_array_de_dados.append(nparray_de_dados)

    array_de_dados_transformada = transformada(array_de_dados)
    array_de_dados_transformada = array_de_dados_transformada[:int(tamanho_do_array / 2)]
    nparray_de_dados_transformada = np.array(array_de_dados_transformada)
    nparray_de_dados_transformada = np.expand_dims(nparray_de_dados_transformada, axis=1)
    lista_array_de_dados_transformada.append(nparray_de_dados_transformada)

def gerar_array_demais_atividades(serie_de_dados,tamanho_do_array,lista_array_de_dados,rotulo_multiplos ,rotulo_tres,rotulo_binario1,rotulo_binario2,lista_array_de_dados_transformada,adicionar_rotulos = None):
    div = math.floor(len(serie_de_dados) / tamanho_do_array)
    a = 0
    b = tamanho_do_array

    for i in range(div):
        array_de_dados = serie_de_dados[a:b]
        nparray_de_dados = np.array(array_de_dados)
        nparray_de_dados = np.expand_dims(nparray_de_dados, axis=1)
        lista_array_de_dados.append(nparray_de_dados)

        array_de_dados_transformada = transformada(array_de_dados)
        array_de_dados_transformada = array_de_dados_transformada[:int(tamanho_do_array/2)]
        nparray_de_dados_transformada = np.array(array_de_dados_transformada)
        nparray_de_dados_transformada = np.expand_dims(nparray_de_dados_transformada, axis=1)
        lista_array_de_dados_transformada.append(nparray_de_dados_transformada)

        if adicionar_rotulos == "sim_acc":

            lista_de_rotulos_multiplo_tempo.append(rotulo_multiplos)
            lista_de_rotulos_tres_labels_tempo.append(rotulo_tres)
            lista_de_rotulos_binario1_tempo.append(rotulo_binario1)
            lista_de_rotulos_binario2_tempo.append(rotulo_binario2)

        elif adicionar_rotulos == "sim_gir":

            lista_de_rotulos_multiplo_freq.append(rotulo_multiplos)
            lista_de_rotulos_tres_labels_freq.append(rotulo_tres)
            lista_de_rotulos_binario1_freq.append(rotulo_binario1)
            lista_de_rotulos_binario2_freq.append(rotulo_binario2)

        a += tamanho_do_array
        b += tamanho_do_array

def seccionar_array_de_dados(df_acc,df_gir,i):
    magacc = df_acc.loc[df_acc["sampling"] == i, "Magnitude"]
    magacc = magacc.reset_index(drop=True)
    magacc = magacc.drop(0)

    xacc = df_acc.loc[df_acc["sampling"] == i, "ax"]
    xacc = xacc.reset_index(drop=True)
    xacc = xacc.drop(0)

    yacc = df_acc.loc[df_acc["sampling"] == i, "ay"]
    yacc = yacc.reset_index(drop=True)
    yacc = yacc.drop(0)

    zacc = df_acc.loc[df_acc["sampling"] == i, "az"]
    zacc = zacc.reset_index(drop=True)
    zacc = zacc.drop(0)

    maggir = df_gir.loc[df_gir["sampling"] == i, "Magnitude"]
    maggir = maggir.reset_index(drop=True)
    maggir = maggir.drop(0)

    xgir = df_gir.loc[df_gir["sampling"] == i, "wx"]
    xgir = xgir.reset_index(drop=True)
    xgir = xgir.drop(0)

    ygir = df_gir.loc[df_gir["sampling"] == i, "wy"]
    ygir = ygir.reset_index(drop=True)
    ygir = ygir.drop(0)

    zgir = df_gir.loc[df_gir["sampling"] == i, "wz"]
    zgir = zgir.reset_index(drop=True)
    zgir = zgir.drop(0)

    timestamp_acc = df_acc.loc[df_acc["sampling"] == i, "timestamp"]
    timestamp_gir = df_gir.loc[df_gir["sampling"] == i, "timestamp"]
    tempo_segundos_acc = gerar_serie_de_tempo(timestamp_acc)
    tempo_segundos_gir = gerar_serie_de_tempo(timestamp_gir)

    return magacc,xacc,yacc,zacc,tempo_segundos_acc,maggir,xgir,ygir,zgir,tempo_segundos_gir

def plotar_grafico_das_atividade(i,lista_de_nomes,df_sampling,magacc,xacc,yacc,zacc,tempo_segundos_acc,maggir,xgir,ygir,zgir,tempo_segundos_gir,
                                 diretorio1, diretorio2, diretorio3, diretorio4, diretorio5,diretorio6,diretorio7,diretorio8,arquivo_erros):
    atividade = (df_sampling.loc[df_sampling["id"] == i, "exercise"].iloc[0])

    if (df_sampling.loc[df_sampling["id"] == i, "withRifle"].iloc[0]) == 1:
        atividade = f'{atividade}_with_rifle'

    nome_figura = f'ID{(df_sampling.loc[df_sampling["id"] == i, "userId"].iloc[0])}_{atividade}'

    lista_de_nomes.append(nome_figura)
    cont = 0
    for j in range(len(lista_de_nomes)):
        if lista_de_nomes[j] == nome_figura:
            cont += 1

    nome_figura_definitivo = f'{nome_figura}.{cont}.png'

    plot_grafico(magacc, tempo_segundos_acc, nome_figura_definitivo, diretorio1, arquivo_erros)
    plot_grafico(xacc, tempo_segundos_acc, nome_figura_definitivo, diretorio2, arquivo_erros)
    plot_grafico(yacc, tempo_segundos_acc, nome_figura_definitivo, diretorio3, arquivo_erros)
    plot_grafico(zacc, tempo_segundos_acc, nome_figura_definitivo, diretorio4, arquivo_erros)

    plot_grafico(maggir, tempo_segundos_gir, nome_figura_definitivo, diretorio5, arquivo_erros)
    plot_grafico(xgir, tempo_segundos_gir, nome_figura_definitivo, diretorio6, arquivo_erros)
    plot_grafico(ygir, tempo_segundos_gir, nome_figura_definitivo, diretorio7, arquivo_erros)
    plot_grafico(zgir, tempo_segundos_gir, nome_figura_definitivo, diretorio8, arquivo_erros)

def criar_conjuntos_de_dados_para_treino(posicao,atividade,magacc,xacc,yacc,zacc,maggir,xgir,ygir,zgir):

    lista_atividades_de_cinco_segundos = ["FALL_1", "FALL_2","FALL_3","FALL_5","FALL_6","ADL_7","ADL_8","ADL_15"]
    lista_atividades_de_transicao = ["OM_3", "OM_4", "OM_5","OM_6", "OM_7", "OM_8"]

    rotulo_multiplos ,rotulo_tres,rotulo_binario1,rotulo_binario2 = gerar_rotulos(atividade)

    tamanho_do_array = 1050 if posicao == "CHEST" else 480

    if len(xgir) >= tamanho_do_array and len(xacc) >= tamanho_do_array:
        if atividade in lista_atividades_de_cinco_segundos:

            valor_maximo_acc = max(magacc)


            gerar_array_de_atividades_de_5s(valor_maximo_acc,atividade,magacc, tamanho_do_array, lista_array_de_dados_magacc,lista_array_de_dados_magacc_transformada,rotulo_multiplos ,rotulo_tres,rotulo_binario1,rotulo_binario2,"sim")
            gerar_array_de_atividades_de_5s(valor_maximo_acc,atividade,xacc, tamanho_do_array, lista_array_de_dados_xacc,lista_array_de_dados_xacc_transformada,rotulo_multiplos ,rotulo_tres,rotulo_binario1,rotulo_binario2)
            gerar_array_de_atividades_de_5s(valor_maximo_acc,atividade,yacc, tamanho_do_array, lista_array_de_dados_yacc,lista_array_de_dados_yacc_transformada,rotulo_multiplos ,rotulo_tres,rotulo_binario1,rotulo_binario2)
            gerar_array_de_atividades_de_5s(valor_maximo_acc,atividade,zacc, tamanho_do_array, lista_array_de_dados_zacc,lista_array_de_dados_zacc_transformada,rotulo_multiplos ,rotulo_tres,rotulo_binario1,rotulo_binario2)
            gerar_array_de_atividades_de_5s(valor_maximo_acc,atividade,maggir, tamanho_do_array, lista_array_de_dados_maggir,lista_array_de_dados_maggir_transformada,rotulo_multiplos ,rotulo_tres,rotulo_binario1,rotulo_binario2)
            gerar_array_de_atividades_de_5s(valor_maximo_acc,atividade,xgir, tamanho_do_array, lista_array_de_dados_xgir,lista_array_de_dados_xgir_transformada,rotulo_multiplos ,rotulo_tres,rotulo_binario1,rotulo_binario2)
            gerar_array_de_atividades_de_5s(valor_maximo_acc,atividade,ygir, tamanho_do_array, lista_array_de_dados_ygir,lista_array_de_dados_ygir_transformada,rotulo_multiplos ,rotulo_tres,rotulo_binario1,rotulo_binario2)
            gerar_array_de_atividades_de_5s(valor_maximo_acc,atividade,zgir, tamanho_do_array, lista_array_de_dados_zgir,lista_array_de_dados_zgir_transformada,rotulo_multiplos ,rotulo_tres,rotulo_binario1,rotulo_binario2)

        elif atividade in lista_atividades_de_transicao:
            gerar_array_de_atividades_de_transicao(magacc, tamanho_do_array, lista_array_de_dados_magacc,lista_array_de_dados_magacc_transformada)

            gerar_array_de_atividades_de_transicao(xacc, tamanho_do_array, lista_array_de_dados_xacc,lista_array_de_dados_xacc_transformada)
            gerar_array_de_atividades_de_transicao(yacc, tamanho_do_array, lista_array_de_dados_yacc,lista_array_de_dados_yacc_transformada)
            gerar_array_de_atividades_de_transicao(zacc, tamanho_do_array, lista_array_de_dados_zacc,lista_array_de_dados_zacc_transformada)
            gerar_array_de_atividades_de_transicao(maggir, tamanho_do_array, lista_array_de_dados_maggir,lista_array_de_dados_maggir_transformada)
            gerar_array_de_atividades_de_transicao(xgir, tamanho_do_array, lista_array_de_dados_xgir,lista_array_de_dados_xgir_transformada)
            gerar_array_de_atividades_de_transicao(ygir, tamanho_do_array, lista_array_de_dados_ygir,lista_array_de_dados_ygir_transformada)
            gerar_array_de_atividades_de_transicao(zgir, tamanho_do_array, lista_array_de_dados_zgir,lista_array_de_dados_zgir_transformada)
            lista_de_rotulos_multiplo_tempo.append(rotulo_multiplos)
            lista_de_rotulos_tres_labels_tempo.append(rotulo_tres)
            lista_de_rotulos_binario1_tempo.append(rotulo_binario1)
            lista_de_rotulos_binario2_tempo.append(rotulo_binario2)
            lista_de_rotulos_multiplo_freq.append(rotulo_multiplos)
            lista_de_rotulos_tres_labels_freq.append(rotulo_tres)
            lista_de_rotulos_binario1_freq.append(rotulo_binario1)
            lista_de_rotulos_binario2_freq.append(rotulo_binario2)
        else:
            gerar_array_demais_atividades(magacc, tamanho_do_array, lista_array_de_dados_magacc, rotulo_multiplos,rotulo_tres, rotulo_binario1, rotulo_binario2,lista_array_de_dados_magacc_transformada,"sim_acc")
            gerar_array_demais_atividades(xacc, tamanho_do_array, lista_array_de_dados_xacc, rotulo_multiplos,rotulo_tres, rotulo_binario1, rotulo_binario2,lista_array_de_dados_xacc_transformada)
            gerar_array_demais_atividades(yacc, tamanho_do_array, lista_array_de_dados_yacc, rotulo_multiplos,rotulo_tres, rotulo_binario1, rotulo_binario2,lista_array_de_dados_yacc_transformada)
            gerar_array_demais_atividades(zacc, tamanho_do_array, lista_array_de_dados_zacc, rotulo_multiplos,rotulo_tres, rotulo_binario1, rotulo_binario2,lista_array_de_dados_zacc_transformada)
            gerar_array_demais_atividades(maggir, tamanho_do_array, lista_array_de_dados_maggir, rotulo_multiplos,rotulo_tres, rotulo_binario1, rotulo_binario2,lista_array_de_dados_maggir_transformada,"sim_gir")
            gerar_array_demais_atividades(xgir, tamanho_do_array, lista_array_de_dados_xgir, rotulo_multiplos,rotulo_tres, rotulo_binario1, rotulo_binario2,lista_array_de_dados_xgir_transformada)
            gerar_array_demais_atividades(ygir, tamanho_do_array, lista_array_de_dados_ygir, rotulo_multiplos,rotulo_tres, rotulo_binario1, rotulo_binario2,lista_array_de_dados_ygir_transformada)
            gerar_array_demais_atividades(zgir, tamanho_do_array, lista_array_de_dados_zgir, rotulo_multiplos,rotulo_tres, rotulo_binario1, rotulo_binario2,lista_array_de_dados_zgir_transformada)


def plotar_atividades(df_acc,df_gir,df_sampling,diretorio1,diretorio2,diretorio3,diretorio4,diretorio5, diretorio6, diretorio7,
                                     diretorio8,arquivo_erros):
    lista_de_nomes = []

    for i in (df_sampling["id"]):


        atividade = (df_sampling.loc[df_sampling["id"] == i, "exercise"].iloc[0])

        magacc,xacc,yacc,zacc,tempo_segundos_acc,maggir,xgir,ygir,zgir,tempo_segundos_gir = seccionar_array_de_dados(df_acc,df_gir,i)

        criar_conjuntos_de_dados_para_treino(posicao, atividade, magacc, xacc, yacc, zacc, maggir, xgir, ygir, zgir)

        #plotar_grafico_das_atividade(i, lista_de_nomes,df_sampling, magacc, xacc, yacc, zacc, tempo_segundos_acc, maggir, xgir,ygir, zgir,
                                     #tempo_segundos_gir,diretorio1, diretorio2, diretorio3, diretorio4, diretorio5, diretorio6, diretorio7,
                                     #diretorio8, arquivo_erros)



diretorio_principal= "/home/dev/Área de trabalho/Combatente/Combatente/Database"

lista_de_subdiretorios = os.listdir(diretorio_principal)

lista_de_subdiretorios.sort(key=ordenar_por_numero)

posicao = "LEFT"

if posicao == "CHEST":
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

elif posicao == "LEFT":
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
lista_array_de_dados_magacc = []
#xacc
lista_array_de_dados_xacc = []
#yacc
lista_array_de_dados_yacc = []
#zacc
lista_array_de_dados_zacc = []

#maggir
lista_array_de_dados_maggir = []
#xgir
lista_array_de_dados_xgir = []
#ygir
lista_array_de_dados_ygir= []
#zgir
lista_array_de_dados_zgir = []

#magacc no dominio da freqência
lista_array_de_dados_magacc_transformada = []
#xacc no dominio da freqência
lista_array_de_dados_xacc_transformada = []
#yacc no dominio da freqência
lista_array_de_dados_yacc_transformada = []
#zacc no dominio da freqência
lista_array_de_dados_zacc_transformada = []

#maggir no dominio da freqência
lista_array_de_dados_maggir_transformada = []
#xgir no dominio da freqência
lista_array_de_dados_xgir_transformada = []
#ygir no dominio da freqência
lista_array_de_dados_ygir_transformada= []
#zgir no dominio da freqência
lista_array_de_dados_zgir_transformada = []

lista_de_rotulos_multiplo_tempo = []
lista_de_rotulos_tres_labels_tempo = []
lista_de_rotulos_binario1_tempo = []
lista_de_rotulos_binario2_tempo = []

lista_de_rotulos_multiplo_freq = []
lista_de_rotulos_tres_labels_freq = []
lista_de_rotulos_binario1_freq = []
lista_de_rotulos_binario2_freq = []


for subdiretorio in lista_de_subdiretorios:
    acc,gir,sampling = obter_caminhos_dos_arquivos(diretorio_principal, subdiretorio, posicao)
    df_acc,df_gir,df_sampling = gerar_dataframe(acc,gir,sampling)
    plotar_atividades(df_acc, df_gir, df_sampling,diretorio1,diretorio2,diretorio3,diretorio4,diretorio5, diretorio6, diretorio7,
                                     diretorio8,arquivo_erros)


conjunto_rotulos_multiplos_tempo = np.asarray(lista_de_rotulos_multiplo_tempo)
conjunto_rotulos_tres_labels_tempo = np.asarray(lista_de_rotulos_tres_labels_tempo)
conjunto_rotulos_binario1_tempo = np.asarray(lista_de_rotulos_binario1_tempo)
conjunto_rotulos_binario2_tempo= np.asarray(lista_de_rotulos_binario2_tempo)

conjunto_rotulos_multiplos_freq = np.asarray(lista_de_rotulos_multiplo_freq )
conjunto_rotulos_tres_labels_freq = np.asarray(lista_de_rotulos_tres_labels_freq )
conjunto_rotulos_binario1_freq = np.asarray(lista_de_rotulos_binario1_freq )
conjunto_rotulos_binario2_freq = np.asarray(lista_de_rotulos_binario2_freq )

np.save(os.path.join(diretorio_rotulos, 'rotulos_multiplos_tempo.npy'), conjunto_rotulos_multiplos_tempo)
np.save(os.path.join(diretorio_rotulos, 'rotulos_tres_labels_tempo.npy'), conjunto_rotulos_tres_labels_tempo)
np.save(os.path.join(diretorio_rotulos, 'rotulos_binario1_tempo.npy'), conjunto_rotulos_binario1_tempo)
np.save(os.path.join(diretorio_rotulos, 'rotulos_binario2_tempo.npy'), conjunto_rotulos_binario2_tempo)

np.save(os.path.join(diretorio_rotulos, 'rotulos_multiplos_freq.npy'), conjunto_rotulos_multiplos_freq)
np.save(os.path.join(diretorio_rotulos, 'rotulos_tres_labels_freq.npy'), conjunto_rotulos_tres_labels_freq)
np.save(os.path.join(diretorio_rotulos, 'rotulos_binario1_freq.npy'), conjunto_rotulos_binario1_freq)
np.save(os.path.join(diretorio_rotulos, 'rotulos_binario2_freq.npy'), conjunto_rotulos_binario2_freq)

conjunto_de_dados_magacc= np.asarray(lista_array_de_dados_magacc)
conjunto_de_dados_magacc_transformada = np.asarray(lista_array_de_dados_magacc_transformada)
conjunto_de_dados_xacc= np.asarray(lista_array_de_dados_xacc)
conjunto_de_dados_xacc_transformada = np.asarray(lista_array_de_dados_xacc_transformada)
conjunto_de_dados_yacc= np.asarray(lista_array_de_dados_yacc)
conjunto_de_dados_yacc_transformada = np.asarray(lista_array_de_dados_yacc_transformada)
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



